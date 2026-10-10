import os
import time
try:
    from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
except ImportError:
    Message = None
    InlineKeyboardMarkup = None
    InlineKeyboardButton = None
from resolvers import format_size
try:
    from core.queue import task_manager, TaskCancelledException
except ImportError:
    task_manager = None
    class TaskCancelledException(Exception):
        pass
from helpers.aria2 import download_with_aria2c

def create_progress_bar(current, total):
    if not total:
        return "[▰▰▰▱▱▱▱▱▱▱] 0%"
    pct = current / total
    filled = min(10, int(pct * 10))
    bar = "▰" * filled + "▱" * (10 - filled)
    return f"[{bar}] {pct * 100:.1f}%"

def get_cancel_button(user_id: int):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Cancel Task", callback_data=f"cancel_{user_id}")]
    ])

class ProgressTracker:
    def __init__(self, message: Message, action_text: str, user_id: int = 0):
        self.message = message
        self.action_text = action_text
        self.user_id = user_id
        self.last_edit = 0
        self.start_time = time.time()

    async def update(self, current, total):
        # 1. Check if user pressed Cancel Task
        if self.user_id and task_manager.is_cancelled(self.user_id):
            raise TaskCancelledException("Task cancelled by user.")

        now = time.time()
        if now - self.last_edit < 2.5:
            return
        self.last_edit = now

        elapsed = max(1.0, now - self.start_time)
        speed = current / elapsed
        speed_str = f"{format_size(speed)}/s"
        bar = create_progress_bar(current, total)
        current_str = format_size(current)
        total_str = format_size(total) if total else "Unknown"

        text = (
            f"<b>{self.action_text}</b>\n\n"
            f"<code>{bar}</code>\n"
            f"💾 <b>Progress:</b> <code>{current_str} / {total_str}</code>\n"
            f"⚡ <b>SSEngine Speed:</b> <code>{speed_str}</code>"
        )
        try:
            markup = get_cancel_button(self.user_id) if self.user_id else None
            await self.message.edit_text(text, reply_markup=markup)
        except Exception:
            pass

async def download_file(url: str, output_path: str, progress_tracker: ProgressTracker, user_id: int = 0, referer: str = "", cookie: str = "") -> str:
    """High-speed DDL download using multi-connection ssengine with real-time progress."""
    return await download_with_aria2c(
        url=url,
        output_path=output_path,
        progress_tracker=progress_tracker,
        user_id=user_id,
        connections=16,
        referer=referer,
        cookie=cookie
    )
