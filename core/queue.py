import os
import time
import asyncio
try:
    from pyrogram import enums
    from pyrogram.types import Message
except ImportError:
    enums = None
    Message = None
import config
from translations import Script

MAX_CONCURRENT_TASKS = getattr(config, "MAX_CONCURRENT_TASKS", 3)
USER_COOLDOWN_SECONDS = getattr(config, "USER_COOLDOWN_SECONDS", 60)

class TaskCancelledException(Exception):
    """Raised when user clicks Cancel Task during download/mux/upload."""
    pass

class TaskQueueManager:
    """
    Manages per-user concurrency (only 1 active task per user),
    task cancellation, automatic hosting storage cleanup,
    cooldown after completion, and global max active tasks with FIFO Queue.
    """
    def __init__(self, max_concurrent: int = 3, cooldown_seconds: int = 60):
        self.max_concurrent = max_concurrent
        self.cooldown_seconds = cooldown_seconds
        self.active_users = set()
        self.cancelled_tasks = set()
        self.user_temp_files = {}  # user_id -> set of file paths
        self.user_cooldowns = {}
        self.queue_waiters = []
        self.active_count = 0
        self.lock = asyncio.Lock()

    def check_user_allowed(self, user_id: int) -> tuple[bool, str, int]:
        if user_id in self.active_users:
            return False, "running", 0

        last_done = self.user_cooldowns.get(user_id)
        if last_done:
            elapsed = time.time() - last_done
            if elapsed < self.cooldown_seconds:
                return False, "cooldown", int(self.cooldown_seconds - elapsed)

        return True, "ok", 0

    def mark_user_active(self, user_id: int):
        self.active_users.add(user_id)
        self.cancelled_tasks.discard(user_id)
        self.user_temp_files[user_id] = set()

    def mark_user_done(self, user_id: int):
        self.active_users.discard(user_id)
        self.cancelled_tasks.discard(user_id)
        self.user_cooldowns[user_id] = time.time()
        self.cleanup_user_files(user_id)

    def register_task_file(self, user_id: int, file_path: str):
        """Registers a temporary file on disk for automatic tracking & cleanup."""
        if not file_path:
            return
        if user_id not in self.user_temp_files:
            self.user_temp_files[user_id] = set()
        self.user_temp_files[user_id].add(os.path.abspath(file_path))

    def is_cancelled(self, user_id: int) -> bool:
        """Checks if user has clicked Cancel Task."""
        return user_id in self.cancelled_tasks

    def cancel_user_task(self, user_id: int) -> bool:
        """
        Immediately cancels the user's active task and wipes all associated
        storage files from the hosting server.
        """
        if user_id not in self.active_users:
            return False

        self.cancelled_tasks.add(user_id)
        # Immediate disk space wipe
        self.cleanup_user_files(user_id)
        return True

    def cleanup_user_files(self, user_id: int):
        """Purges all temporary files created for this user on the server."""
        files_to_remove = self.user_temp_files.pop(user_id, set())
        for f in files_to_remove:
            if f and os.path.exists(f):
                try:
                    if os.path.isdir(f):
                        import shutil
                        shutil.rmtree(f, ignore_errors=True)
                    else:
                        os.remove(f)
                except Exception as e:
                    print(f"[STORAGE CLEANUP NOTE] Failed to delete {f}: {e}")

    async def acquire_slot(self, user_id: int, status_message: Message = None) -> int:
        async with self.lock:
            if self.active_count < self.max_concurrent:
                self.active_count += 1
                return 0

            event = asyncio.Event()
            self.queue_waiters.append((user_id, event))
            queue_pos = len(self.queue_waiters)

        if status_message:
            try:
                await status_message.edit_text(
                    Script.TASK_QUEUED_TXT.format(queue_pos),
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception:
                pass

        await event.wait()
        return queue_pos

    async def release_slot(self, user_id: int):
        next_event = None
        async with self.lock:
            self.mark_user_done(user_id)
            if self.queue_waiters:
                next_user, next_event = self.queue_waiters.pop(0)
            else:
                self.active_count = max(0, self.active_count - 1)

        if next_event:
            next_event.set()

task_manager = TaskQueueManager(
    max_concurrent=MAX_CONCURRENT_TASKS,
    cooldown_seconds=USER_COOLDOWN_SECONDS
)
