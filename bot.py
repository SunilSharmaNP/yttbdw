# ==============================================================================
# 🤖 Bot Developer / Owner : Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ
# 🌐 Developer URL        : https://t.me/Sunil_Sharma_2_0_Bot (@Sunil_Sharma_2_0_Bot)
# 📢 Telegram Channel     : https://t.me/SSBotsUpdates (@SSBotsUpdates)
# 📺 YouTube Channel      : https://www.youtube.com/@SunilWebTricks (SunilWebTricks)
# 💬 Ask Doubt / Contact   : @Sunil_Sharma_2_0_Bot
# ==============================================================================

"""
Main Executable Entry Point for TeraBox, Diskwala & YouTube Downloader Bot.
Dual Channel Force-Subscription Verification (Updates + Deals Channel)
High-Speed Chunked Download & 2GB Telegram MTProto Upload
Powered by Sunil-SSBots Custom Engine (https://sunil-ssbots.vercel.app)
"""

import os
import sys
import shutil

# Ensure local directory is prioritized in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Auto-detect or inject FFmpeg into PATH if missing
if not shutil.which("ffmpeg"):
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
        print("[INIT] FFmpeg loaded via static_ffmpeg binary.")
    except Exception:
        pass

import time
import json
import re
import math
import asyncio
from datetime import datetime
import aiohttp
import aiofiles

from pyrogram import Client, filters, enums
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import config
from translations import (
    Script,
    get_start_buttons,
    get_help_buttons,
    get_about_buttons,
    get_fsub_buttons,
    get_youtube_quality_buttons
)
from resolvers import (
    extract_urls,
    detect_link_type,
    resolve_terabox,
    resolve_diskwala,
    resolve_youtube,
    format_size
)

# --- Safe Fallback Variable Bindings (Prevents AttributeError on Heroku) ---
API_ID = getattr(config, "API_ID", 0)
API_HASH = getattr(config, "API_HASH", "")
BOT_TOKEN = getattr(config, "BOT_TOKEN", "")
SESSION_STRING = getattr(config, "SESSION_STRING", "")
OWNER_ID = getattr(config, "OWNER_ID", 2032446867)
OWNER_USERNAME = getattr(config, "OWNER_USERNAME", "Sunil_Sharma_2_0_Bot")
SUDO_USERS = getattr(config, "SUDO_USERS", [OWNER_ID])
UPDATES_CHANNEL = getattr(config, "UPDATES_CHANNEL", "SSBotsUpdates")
DEALS_CHANNEL = getattr(config, "DEALS_CHANNEL", "Tg_Shoping")
DEVELOPER_NAME = getattr(config, "DEVELOPER_NAME", "Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ")
DEVELOPER_URL = getattr(config, "DEVELOPER_URL", "https://t.me/Sunil_Sharma_2_0_Bot")
CHANNEL_URL = getattr(config, "CHANNEL_URL", "https://t.me/SSBotsUpdates")
YOUTUBE_URL = getattr(config, "YOUTUBE_URL", "https://www.youtube.com/@SunilWebTricks")
SUPPORT_CHAT = getattr(config, "SUPPORT_CHAT", "Sunil_Sharma_2_0_Bot")
LOG_CHANNEL = getattr(config, "LOG_CHANNEL", None)
DOWNLOAD_DIR = getattr(config, "DOWNLOAD_DIR", "./downloads")
MAX_FILE_SIZE_MB = getattr(config, "MAX_FILE_SIZE_MB", 2048)
TERABOX_API_URL = getattr(config, "TERABOX_API_URL", "https://sunil-ssbots.vercel.app/api/terabox")
DISKWALA_API_URL = getattr(config, "DISKWALA_API_URL", "https://sunil-ssbots.vercel.app/api/diskwala")
YOUTUBE_API_URL = getattr(config, "YOUTUBE_API_URL", "https://sunil-ssbots.vercel.app/api/youtube")
START_PIC = getattr(config, "START_PIC", "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1200&auto=format&fit=crop")
MAX_CONCURRENT_TASKS = getattr(config, "MAX_CONCURRENT_TASKS", 3)
USER_COOLDOWN_SECONDS = getattr(config, "USER_COOLDOWN_SECONDS", 60)
MONGO_URI = getattr(config, "MONGO_URI", "")

# In-Memory Sets for Sudo Admins, Banned Users & Registered Users
sudo_users_set = set(SUDO_USERS)
if OWNER_ID not in sudo_users_set:
    sudo_users_set.add(OWNER_ID)

banned_users_set = set()
registered_users_set = set()
bot_start_time = time.time()

# Optional MongoDB Database Connection
mongo_client = None
db = None
if MONGO_URI:
    try:
        import pymongo
        mongo_client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = mongo_client["ss_downloader_bot"]
        print("[MONGODB] Connected to MongoDB database successfully.")

        # Load persisted sudo users
        try:
            for s in db.sudo_users.find({}, {"user_id": 1}):
                if "user_id" in s:
                    sudo_users_set.add(int(s["user_id"]))
        except Exception:
            pass

        # Load persisted banned users
        try:
            for b in db.banned_users.find({}, {"user_id": 1}):
                if "user_id" in b:
                    banned_users_set.add(int(b["user_id"]))
        except Exception:
            pass

        # Load persisted registered users
        try:
            for u in db.users.find({}, {"user_id": 1}):
                if "user_id" in u:
                    registered_users_set.add(int(u["user_id"]))
        except Exception:
            pass
    except Exception as e:
        print(f"[MONGODB NOTE] Connection failed or skipped: {e}")

def is_admin(user_id: int) -> bool:
    """Returns True if user is bot owner or in sudo admins."""
    return user_id == OWNER_ID or user_id in sudo_users_set

def is_banned(user_id: int) -> bool:
    """Returns True if user is banned from using the bot."""
    return user_id in banned_users_set

def add_sudo_user(user_id: int):
    """Adds a new sudo admin in-memory and in MongoDB."""
    sudo_users_set.add(user_id)
    if db is not None:
        try:
            db.sudo_users.update_one(
                {"user_id": user_id},
                {"$set": {"user_id": user_id, "added_at": time.time()}},
                upsert=True
            )
        except Exception:
            pass

def remove_sudo_user(user_id: int):
    """Removes a sudo admin in-memory and in MongoDB."""
    sudo_users_set.discard(user_id)
    if db is not None:
        try:
            db.sudo_users.delete_one({"user_id": user_id})
        except Exception:
            pass

def ban_user(user_id: int, reason: str = "", admin_id: int = 0):
    """Bans a user in-memory and in MongoDB."""
    banned_users_set.add(user_id)
    if db is not None:
        try:
            db.banned_users.update_one(
                {"user_id": user_id},
                {"$set": {
                    "user_id": user_id,
                    "reason": reason,
                    "banned_by": admin_id,
                    "banned_at": time.time()
                }},
                upsert=True
            )
        except Exception:
            pass

def unban_user(user_id: int):
    """Unbans a user in-memory and in MongoDB."""
    banned_users_set.discard(user_id)
    if db is not None:
        try:
            db.banned_users.delete_one({"user_id": user_id})
        except Exception:
            pass

def db_add_user(user_id: int, user_name: str, username: str = "") -> bool:
    """
    Registers a user. Returns True if this is a newly registered user (first time).
    """
    is_new = user_id not in registered_users_set
    registered_users_set.add(user_id)
    if db is not None:
        try:
            existing = db.users.find_one({"user_id": user_id})
            if existing is None:
                is_new = True
            db.users.update_one(
                {"user_id": user_id},
                {"$set": {
                    "name": user_name,
                    "username": username,
                    "last_active": time.time()
                }},
                upsert=True
            )
        except Exception:
            pass
    return is_new

def db_log_download(user_id: int, provider: str, file_name: str, size: str):
    if db is not None:
        try:
            db.downloads.insert_one({
                "user_id": user_id,
                "provider": provider,
                "file_name": file_name,
                "size": size,
                "timestamp": time.time()
            })
        except Exception:
            pass

async def send_log(client: Client, text: str):
    """Safely dispatches log notifications to LOG_CHANNEL."""
    if not LOG_CHANNEL or not client:
        return
    try:
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=text,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML
        )
    except FloodWait as e:
        try:
            await asyncio.sleep(e.value)
            await client.send_message(
                chat_id=LOG_CHANNEL,
                text=text,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            pass
    except Exception as e:
        print(f"[LOG CHANNEL NOTE] {e}")

async def log_bot_started(client: Client):
    """Sends bot started notification to LOG_CHANNEL."""
    if not LOG_CHANNEL or not client:
        return
    try:
        me = getattr(client, "me", None) or await client.get_me()
        bot_name = me.first_name or "SS Downloader Bot"
        bot_username = me.username or "Bot"
        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        db_status = "Connected (MongoDB)" if db is not None else "In-Memory Fallback"

        text = Script.LOG_BOT_STARTED_TXT.format(
            bot_name=bot_name,
            bot_username=bot_username,
            owner_id=OWNER_ID,
            max_tasks=MAX_CONCURRENT_TASKS,
            cooldown=USER_COOLDOWN_SECONDS,
            db_status=db_status,
            timestamp=now_str
        )
        await send_log(client, text)
    except Exception as e:
        print(f"[LOG BOT STARTED WARNING] {e}")

# In-memory cache for pending YouTube quality selections
# cache_id -> {title, author, thumbnail, download_links, user_id}
yt_cache = {}

# Initialize Pyrogram MTProto Client
if SESSION_STRING:
    app = Client(
        name="terabox_session",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING
    )
elif BOT_TOKEN:
    app = Client(
        name="terabox_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )
else:
    app = None
    print("[WARNING] API_ID/API_HASH and BOT_TOKEN or SESSION_STRING not set in .env")

# --- Force Subscribe Verification Helper ---

async def get_channel_invite(client: Client, channel_target):
    """Returns a valid link for a channel (public t.me link or created invite link)"""
    try:
        if str(channel_target).startswith("-100") or str(channel_target).lstrip("-").isdigit():
            chat = await client.get_chat(int(channel_target))
            if chat.username:
                return f"https://t.me/{chat.username}"
            invite = await client.create_chat_invite_link(int(channel_target))
            return invite.invite_link
        else:
            clean_name = str(channel_target).lstrip("@")
            return f"https://t.me/{clean_name}"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await get_channel_invite(client, channel_target)
    except Exception:
        clean_name = str(channel_target).lstrip("@")
        return f"https://t.me/{clean_name}"

async def check_membership(client: Client, channel_target, user_id: int) -> bool:
    """Checks if a user is joined in a specific channel"""
    if not channel_target:
        return True
    try:
        chat_id = int(channel_target) if (str(channel_target).startswith("-100") or str(channel_target).lstrip("-").isdigit()) else f"@{str(channel_target).lstrip('@')}"
        member = await client.get_chat_member(chat_id=chat_id, user_id=user_id)
        if member.status in (enums.ChatMemberStatus.BANNED, enums.ChatMemberStatus.LEFT):
            return False
        return True
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"[FSUB NOTE] Channel check warning ({channel_target}): {e}")
        return True

async def check_fsub(client: Client, user_id: int):
    """Verifies both Updates and Deals channels"""
    updates_ok = await check_membership(client, UPDATES_CHANNEL, user_id)
    deals_ok = await check_membership(client, DEALS_CHANNEL, user_id)
    is_fully_joined = updates_ok and deals_ok
    return is_fully_joined, updates_ok, deals_ok

# Helper for progress visualization
def create_progress_bar(current, total):
    if not total:
        return "[▰▰▰▱▱▱▱▱▱▱] 0%"
    pct = current / total
    filled = min(10, int(pct * 10))
    bar = "▰" * filled + "▱" * (10 - filled)
    return f"[{bar}] {pct * 100:.1f}%"

class ProgressTracker:
    def __init__(self, message: Message, action_text: str):
        self.message = message
        self.action_text = action_text
        self.last_edit = 0
        self.start_time = time.time()

    async def update(self, current, total):
        now = time.time()
        if now - self.last_edit < 3.5:
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
            f"⚡ <b>Speed:</b> <code>{speed_str}</code>"
        )
        try:
            await self.message.edit_text(text)
        except Exception:
            pass

async def download_file(url: str, output_path: str, progress_tracker: ProgressTracker):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    timeout = aiohttp.ClientTimeout(total=3600)
    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status not in (200, 206):
                raise Exception(f"Download HTTP error {resp.status}")
            total = int(resp.headers.get("content-length") or 0)
            received = 0
            async with aiofiles.open(output_path, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 1024):
                    await f.write(chunk)
                    received += len(chunk)
                    await progress_tracker.update(received, total)
    return output_path

async def mux_media_ffmpeg(video_path: str, audio_path: str, output_path: str) -> bool:
    """
    Ultra-fast muxing of video stream and audio stream using FFmpeg.
    Uses stream copy (-c copy) when codecs permit (0% CPU re-encoding, takes < 1 second).
    Falls back to AAC audio encode if container requires conversion.
    """
    try:
        # 1. First attempt: Stream Copy (Instantaneous, Lossless)
        cmd_copy = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c", "copy",
            "-map", "0:v:0",
            "-map", "1:a:0?",
            "-shortest",
            output_path
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd_copy,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.communicate()
        if proc.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            return True

        # 2. Second attempt: Video copy with AAC audio encoder
        cmd_aac = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0?",
            "-shortest",
            output_path
        ]
        proc2 = await asyncio.create_subprocess_exec(
            *cmd_aac,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc2.communicate()
        if proc2.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            return True
    except Exception as e:
        print(f"[FFMPEG MUX ERROR] {e}")

    return False

async def convert_to_mp3_ffmpeg(audio_path: str, output_path: str) -> bool:
    """Converts downloaded audio stream to standard 192k MP3 using FFmpeg"""
    try:
        cmd = [
            "ffmpeg", "-y",
            "-i", audio_path,
            "-vn",
            "-acodec", "libmp3lame",
            "-b:a", "192k",
            output_path
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.communicate()
        if proc.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            return True
    except Exception as e:
        print(f"[FFMPEG MP3 ERROR] {e}")
    return False

async def get_video_metadata(video_path: str) -> dict:
    """
    Extracts video duration (in seconds), width, height, and thumbnail using ffprobe/ffmpeg.
    Fixes the TeraBox '00:00' duration bug by inspecting container format & stream headers.
    Also extracts a clean snapshot thumbnail from the video for the Telegram video player!
    """
    duration = 0
    width = 1280
    height = 720
    thumb_path = None

    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,duration",
            "-show_entries", "format=duration",
            "-of", "json",
            video_path
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        if proc.returncode == 0 and stdout:
            data = json.loads(stdout.decode())
            dur_str = data.get("format", {}).get("duration")
            if not dur_str and data.get("streams"):
                dur_str = data["streams"][0].get("duration")
            if dur_str:
                duration = int(float(dur_str))

            if data.get("streams") and len(data["streams"]) > 0:
                s0 = data["streams"][0]
                width = int(s0.get("width") or 1280)
                height = int(s0.get("height") or 720)
    except Exception as e:
        print(f"[FFPROBE METADATA ERROR] {e}")

    # Fallback 1: ffmpeg -i parsing if ffprobe returned 0 duration
    if duration == 0:
        try:
            cmd_info = ["ffmpeg", "-i", video_path]
            proc_info = await asyncio.create_subprocess_exec(
                *cmd_info,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            _, stderr = await proc_info.communicate()
            match_dur = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", stderr.decode("utf-8", errors="ignore"))
            if match_dur:
                hours = int(match_dur.group(1))
                minutes = int(match_dur.group(2))
                seconds = float(match_dur.group(3))
                duration = int(hours * 3600 + minutes * 60 + seconds)
        except Exception as e:
            print(f"[FFMPEG DURATION PARSE ERROR] {e}")

    # Fallback 2: Faststart remux for TeraBox videos (fixes moov atom & 00:00 duration)
    if duration == 0 and os.path.exists(video_path):
        try:
            faststart_temp = video_path + ".faststart.mp4"
            cmd_fast = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-c", "copy",
                "-movflags", "+faststart",
                faststart_temp
            ]
            proc_f = await asyncio.create_subprocess_exec(
                *cmd_fast,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc_f.communicate()
            if proc_f.returncode == 0 and os.path.exists(faststart_temp) and os.path.getsize(faststart_temp) > 1000:
                os.replace(faststart_temp, video_path)
                cmd_recheck = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", video_path]
                proc_r = await asyncio.create_subprocess_exec(
                    *cmd_recheck,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                sout, _ = await proc_r.communicate()
                if sout:
                    d_obj = json.loads(sout.decode())
                    d_str = d_obj.get("format", {}).get("duration")
                    if d_str:
                        duration = int(float(d_str))
        except Exception as e:
            print(f"[FASTSTART DURATION FIX NOTE] {e}")

    # Generate a thumbnail frame with ffmpeg
    try:
        ts = int(time.time())
        t_path = os.path.join(DOWNLOAD_DIR, f"{ts}_thumb.jpg")
        seek_sec = "00:00:02" if duration > 3 else "00:00:00.5"
        cmd_thumb = [
            "ffmpeg", "-y",
            "-ss", seek_sec,
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            t_path
        ]
        proc_t = await asyncio.create_subprocess_exec(
            *cmd_thumb,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc_t.communicate()
        if proc_t.returncode == 0 and os.path.exists(t_path) and os.path.getsize(t_path) > 100:
            thumb_path = t_path
    except Exception as e:
        print(f"[THUMBNAIL EXTRACTION ERROR] {e}")

    return {
        "duration": duration,
        "width": width,
        "height": height,
        "thumb": thumb_path
    }

class TaskQueueManager:
    """
    Manages per-user concurrency (only 1 active task per user),
    1-minute cooldown after task completion, and global max 3 active tasks with FIFO Queue.
    Supports MongoDB for persistent user cooldowns across bot restarts.
    """
    def __init__(self, max_concurrent: int = 3, cooldown_seconds: int = 60):
        self.max_concurrent = max_concurrent
        self.cooldown_seconds = cooldown_seconds
        self.active_users = set()
        self.user_cooldowns = {}
        self.queue_waiters = []
        self.active_count = 0
        self.lock = asyncio.Lock()

    def check_user_allowed(self, user_id: int) -> tuple[bool, str, int]:
        if user_id in self.active_users:
            return False, "running", 0

        # Check in-memory or mongo cooldown
        last_done = self.user_cooldowns.get(user_id)
        if not last_done and db is not None:
            try:
                rec = db.cooldowns.find_one({"user_id": user_id})
                if rec and "last_done" in rec:
                    last_done = rec["last_done"]
                    self.user_cooldowns[user_id] = last_done
            except Exception:
                pass

        if last_done:
            elapsed = time.time() - last_done
            if elapsed < self.cooldown_seconds:
                return False, "cooldown", int(self.cooldown_seconds - elapsed)

        return True, "ok", 0

    def mark_user_active(self, user_id: int):
        self.active_users.add(user_id)

    def mark_user_done(self, user_id: int):
        self.active_users.discard(user_id)
        now = time.time()
        self.user_cooldowns[user_id] = now
        if db is not None:
            try:
                db.cooldowns.update_one(
                    {"user_id": user_id},
                    {"$set": {"last_done": now}},
                    upsert=True
                )
            except Exception:
                pass

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

if app:
    # --- Command: /start ---
    @app.on_message(filters.command("start") & filters.private)
    async def start_handler(client: Client, message: Message):
        user = message.from_user
        user_id = user.id
        if is_banned(user_id):
            return await message.reply_text(
                Script.USER_BANNED_ALERT_TXT,
                parse_mode=enums.ParseMode.HTML
            )

        user_name = (user.first_name or "User").replace("<", "&lt;").replace(">", "&gt;")
        username = user.username or "None"

        # Log new user if first time interacting with bot
        is_new = db_add_user(user_id, user_name, username)
        if is_new:
            total_users = len(registered_users_set)
            if db is not None:
                try:
                    total_users = db.users.count_documents({})
                except Exception:
                    pass
            now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            await send_log(
                client,
                Script.LOG_NEW_USER_TXT.format(
                    user_id=user_id,
                    name=user_name,
                    username=username,
                    total_users=total_users,
                    timestamp=now_str
                )
            )

        # 1. Check Dual Force-Sub
        is_joined, _, _ = await check_fsub(client, user_id)
        if not is_joined:
            updates_link = await get_channel_invite(client, UPDATES_CHANNEL)
            deals_link = await get_channel_invite(client, DEALS_CHANNEL)
            buttons = get_fsub_buttons(updates_link, deals_link, user_id)
            try:
                await message.reply_photo(
                    photo=START_PIC,
                    caption=Script.FORCE_SUB_TXT.format(user_name),
                    reply_markup=buttons,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception:
                await message.reply_text(
                    text=Script.FORCE_SUB_TXT.format(user_name),
                    reply_markup=buttons,
                    disable_web_page_preview=True,
                    parse_mode=enums.ParseMode.HTML
                )
            return

        # 2. Main Start Menu with Photo Banner
        bot_info = getattr(client, "me", None) or await client.get_me()
        bot_username = bot_info.username or "Bot"
        buttons = get_start_buttons(bot_username)

        try:
            await message.reply_photo(
                photo=START_PIC,
                caption=Script.START_TXT.format(user_name),
                reply_markup=buttons,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            await message.reply_text(
                text=Script.START_TXT.format(user_name),
                reply_markup=buttons,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )

    # --- Command: /help ---
    @app.on_message(filters.command("help") & filters.private)
    async def help_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if is_banned(user_id):
            return await message.reply_text(Script.USER_BANNED_ALERT_TXT, parse_mode=enums.ParseMode.HTML)

        user_name = message.from_user.first_name or "User"
        is_joined, _, _ = await check_fsub(client, user_id)
        if not is_joined:
            updates_link = await get_channel_invite(client, UPDATES_CHANNEL)
            deals_link = await get_channel_invite(client, DEALS_CHANNEL)
            buttons = get_fsub_buttons(updates_link, deals_link, user_id)
            try:
                return await message.reply_photo(
                    photo=START_PIC,
                    caption=Script.FORCE_SUB_TXT.format(user_name),
                    reply_markup=buttons,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception:
                return await message.reply_text(
                    text=Script.FORCE_SUB_TXT.format(user_name),
                    reply_markup=buttons,
                    disable_web_page_preview=True
                )

        try:
            await message.reply_photo(
                photo=START_PIC,
                caption=Script.HELP_TXT.format(SUPPORT_CHAT),
                reply_markup=get_help_buttons(),
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            await message.reply_text(
                text=Script.HELP_TXT.format(SUPPORT_CHAT),
                reply_markup=get_help_buttons(),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )

    # --- Command: /about ---
    @app.on_message(filters.command("about") & filters.private)
    async def about_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if is_banned(user_id):
            return await message.reply_text(Script.USER_BANNED_ALERT_TXT, parse_mode=enums.ParseMode.HTML)

        user_name = message.from_user.first_name or "User"
        is_joined, _, _ = await check_fsub(client, user_id)
        if not is_joined:
            updates_link = await get_channel_invite(client, UPDATES_CHANNEL)
            deals_link = await get_channel_invite(client, DEALS_CHANNEL)
            buttons = get_fsub_buttons(updates_link, deals_link, user_id)
            try:
                return await message.reply_photo(
                    photo=START_PIC,
                    caption=Script.FORCE_SUB_TXT.format(user_name),
                    reply_markup=buttons,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception:
                return await message.reply_text(
                    text=Script.FORCE_SUB_TXT.format(user_name),
                    reply_markup=buttons,
                    disable_web_page_preview=True
                )

        bot_info = getattr(client, "me", None) or await client.get_me()
        bot_username = bot_info.username or "Bot"
        bot_name = bot_info.first_name or "Media Downloader"
        try:
            await message.reply_photo(
                photo=START_PIC,
                caption=Script.ABOUT_TXT.format(bot_username, bot_name),
                reply_markup=get_about_buttons(),
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            await message.reply_text(
                text=Script.ABOUT_TXT.format(bot_username, bot_name),
                reply_markup=get_about_buttons(),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )

    # --- Command: /ping ---
    @app.on_message(filters.command("ping") & filters.private)
    async def ping_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if is_banned(user_id):
            return await message.reply_text(Script.USER_BANNED_ALERT_TXT, parse_mode=enums.ParseMode.HTML)
        await message.reply_text("🏓 <b>Pong!</b> TeraBox, Diskwala & YouTube Downloader Bot is Online.")

    # --- Command: /ban (Owner & Sudo Admins) ---
    @app.on_message(filters.command("ban") & filters.private)
    async def ban_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            return await message.reply_text(Script.ADMIN_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        target_id = None
        target_name = "User"
        reason = "No reason provided"

        if message.reply_to_message and message.reply_to_message.from_user:
            target_id = message.reply_to_message.from_user.id
            target_name = message.reply_to_message.from_user.first_name or f"User {target_id}"
            if len(message.command) > 1:
                reason = " ".join(message.command[1:])
        elif len(message.command) > 1:
            try:
                target_id = int(message.command[1])
                target_name = f"User {target_id}"
                if len(message.command) > 2:
                    reason = " ".join(message.command[2:])
            except ValueError:
                return await message.reply_text(Script.BAN_USAGE_TXT, parse_mode=enums.ParseMode.HTML)
        else:
            return await message.reply_text(Script.BAN_USAGE_TXT, parse_mode=enums.ParseMode.HTML)

        if target_id == OWNER_ID or target_id in sudo_users_set:
            return await message.reply_text(Script.CANNOT_BAN_ADMIN, parse_mode=enums.ParseMode.HTML)

        if is_banned(target_id):
            return await message.reply_text(Script.ALREADY_BANNED.format(user_id=target_id), parse_mode=enums.ParseMode.HTML)

        ban_user(target_id, reason, user_id)
        admin_name = message.from_user.first_name or "Admin"

        await message.reply_text(
            Script.USER_BANNED_SUCCESS.format(user_id=target_id, reason=reason),
            parse_mode=enums.ParseMode.HTML
        )

        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        await send_log(
            client,
            Script.LOG_USER_BANNED_TXT.format(
                user_id=target_id,
                name=target_name,
                admin_id=user_id,
                admin_name=admin_name,
                reason=reason,
                timestamp=now_str
            )
        )

    # --- Command: /unban (Owner & Sudo Admins) ---
    @app.on_message(filters.command("unban") & filters.private)
    async def unban_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            return await message.reply_text(Script.ADMIN_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        target_id = None
        target_name = "User"

        if message.reply_to_message and message.reply_to_message.from_user:
            target_id = message.reply_to_message.from_user.id
            target_name = message.reply_to_message.from_user.first_name or f"User {target_id}"
        elif len(message.command) > 1:
            try:
                target_id = int(message.command[1])
                target_name = f"User {target_id}"
            except ValueError:
                return await message.reply_text(Script.UNBAN_USAGE_TXT, parse_mode=enums.ParseMode.HTML)
        else:
            return await message.reply_text(Script.UNBAN_USAGE_TXT, parse_mode=enums.ParseMode.HTML)

        if not is_banned(target_id):
            return await message.reply_text(Script.NOT_BANNED.format(user_id=target_id), parse_mode=enums.ParseMode.HTML)

        unban_user(target_id)
        admin_name = message.from_user.first_name or "Admin"

        await message.reply_text(
            Script.USER_UNBANNED_SUCCESS.format(user_id=target_id),
            parse_mode=enums.ParseMode.HTML
        )

        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        await send_log(
            client,
            Script.LOG_USER_UNBANNED_TXT.format(
                user_id=target_id,
                name=target_name,
                admin_id=user_id,
                admin_name=admin_name,
                timestamp=now_str
            )
        )

    # --- Command: /addsudo (Owner Only) ---
    @app.on_message(filters.command("addsudo") & filters.private)
    async def addsudo_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if user_id != OWNER_ID:
            return await message.reply_text(Script.OWNER_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        target_id = None
        if message.reply_to_message and message.reply_to_message.from_user:
            target_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                target_id = int(message.command[1])
            except ValueError:
                return await message.reply_text(Script.ADDSUDO_USAGE_TXT, parse_mode=enums.ParseMode.HTML)
        else:
            return await message.reply_text(Script.ADDSUDO_USAGE_TXT, parse_mode=enums.ParseMode.HTML)

        if target_id in sudo_users_set:
            return await message.reply_text(f"⚠️ <b>ᴜsᴇʀ <code>{target_id}</code> ɪs ᴀʟʀᴇᴀᴅʏ ᴀ sᴜᴅᴏ ᴀᴅᴍɪɴ!</b>", parse_mode=enums.ParseMode.HTML)

        add_sudo_user(target_id)
        await message.reply_text(f"✨ <b>ᴜsᴇʀ <code>{target_id}</code> ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ sᴜᴅᴏ ᴀᴅᴍɪɴs!</b>", parse_mode=enums.ParseMode.HTML)

    # --- Command: /delsudo (Owner Only) ---
    @app.on_message(filters.command("delsudo") & filters.private)
    async def delsudo_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if user_id != OWNER_ID:
            return await message.reply_text(Script.OWNER_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        target_id = None
        if message.reply_to_message and message.reply_to_message.from_user:
            target_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                target_id = int(message.command[1])
            except ValueError:
                return await message.reply_text(Script.DELSUDO_USAGE_TXT, parse_mode=enums.ParseMode.HTML)
        else:
            return await message.reply_text(Script.DELSUDO_USAGE_TXT, parse_mode=enums.ParseMode.HTML)

        if target_id == OWNER_ID:
            return await message.reply_text("⚠️ <b>ʏᴏᴜ ᴄᴀɴɴᴏᴛ ʀᴇᴍᴏᴠᴇ ᴛʜᴇ ʙᴏᴛ ᴏᴡɴᴇʀ ғʀᴏᴍ sᴜᴅᴏ!</b>", parse_mode=enums.ParseMode.HTML)

        if target_id not in sudo_users_set:
            return await message.reply_text(f"⚠️ <b>ᴜsᴇʀ <code>{target_id}</code> ɪs ɴᴏᴛ ᴀ sᴜᴅᴏ ᴀᴅᴍɪɴ!</b>", parse_mode=enums.ParseMode.HTML)

        remove_sudo_user(target_id)
        await message.reply_text(f"🗑️ <b>ᴜsᴇʀ <code>{target_id}</code> ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ sᴜᴅᴏ ᴀᴅᴍɪɴs!</b>", parse_mode=enums.ParseMode.HTML)

    # --- Command: /sudolist or /admins (Owner & Sudo Admins) ---
    @app.on_message(filters.command(["sudolist", "admins"]) & filters.private)
    async def sudolist_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            return await message.reply_text(Script.ADMIN_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        admins_text = f"👑 <b>ᴏᴡɴᴇʀ :</b> <code>{OWNER_ID}</code> (@{OWNER_USERNAME})\n\n🛡️ <b>sᴜᴅᴏ ᴀᴅᴍɪɴs ({len(sudo_users_set)}):</b>\n"
        for s_id in sorted(sudo_users_set):
            marker = " (Owner)" if s_id == OWNER_ID else ""
            admins_text += f"• <code>{s_id}</code>{marker}\n"

        await message.reply_text(admins_text, parse_mode=enums.ParseMode.HTML)

    # --- Command: /banlist or /banned (Owner & Sudo Admins) ---
    @app.on_message(filters.command(["banlist", "banned"]) & filters.private)
    async def banlist_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            return await message.reply_text(Script.ADMIN_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        if not banned_users_set:
            return await message.reply_text("🟢 <b>ɴᴏ ᴜsᴇʀs ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ ʙᴀɴɴᴇᴅ!</b>", parse_mode=enums.ParseMode.HTML)

        text = f"🚫 <b>ʙᴀɴɴᴇᴅ ᴜsᴇʀs ({len(banned_users_set)}):</b>\n\n"
        for b_id in sorted(banned_users_set):
            text += f"• <code>{b_id}</code>\n"

        await message.reply_text(text, parse_mode=enums.ParseMode.HTML)

    # --- Command: /stats (Owner & Sudo Admins) ---
    @app.on_message(filters.command("stats") & filters.private)
    async def stats_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            return await message.reply_text(Script.ADMIN_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        total_users = len(registered_users_set)
        total_downloads = 0
        if db is not None:
            try:
                total_users = db.users.count_documents({})
                total_downloads = db.downloads.count_documents({})
            except Exception:
                pass

        uptime_sec = int(time.time() - bot_start_time)
        hrs = uptime_sec // 3600
        mins = (uptime_sec % 3600) // 60
        secs = uptime_sec % 60
        uptime_str = f"{hrs}h {mins}m {secs}s"

        active_count = task_manager.active_count
        queue_count = len(task_manager.queue_waiters)
        banned_count = len(banned_users_set)
        sudo_count = len(sudo_users_set)

        db_type = "MongoDB (Persistent)" if db is not None else "In-Memory"
        log_channel_str = f"<code>{LOG_CHANNEL}</code>" if LOG_CHANNEL else "<i>Not Set</i>"

        text = (
            "📊 ── <b>ʙᴏᴛ sʏsᴛᴇᴍ sᴛᴀᴛɪsᴛɪᴄs</b> ── 📊\n\n"
            f"👥 <b>ᴛᴏᴛᴀʟ ᴜsᴇʀs :</b> <code>{total_users}</code>\n"
            f"📥 <b>ᴛᴏᴛᴀʟ ᴅᴏᴡɴʟᴏᴀᴅs :</b> <code>{total_downloads}</code>\n"
            f"⚡ <b>ᴀᴄᴛɪᴠᴇ ᴛᴀsᴋs :</b> <code>{active_count} / {MAX_CONCURRENT_TASKS}</code>\n"
            f"⏳ <b>ǫᴜᴇᴜᴇᴅ ᴛᴀsᴋs :</b> <code>{queue_count}</code>\n"
            f"🚫 <b>ʙᴀɴɴᴇᴅ ᴜsᴇʀs :</b> <code>{banned_count}</code>\n"
            f"🛡️ <b>sᴜᴅᴏ ᴀᴅᴍɪɴs :</b> <code>{sudo_count}</code>\n"
            f"📢 <b>ʟᴏɢ ᴄʜᴀɴɴᴇʟ :</b> {log_channel_str}\n"
            f"🗄️ <b>ᴅᴀᴛᴀʙᴀsᴇ :</b> <code>{db_type}</code>\n"
            f"⏱️ <b>ᴜᴘᴛɪᴍᴇ :</b> <code>{uptime_str}</code>"
        )
        await message.reply_text(text, parse_mode=enums.ParseMode.HTML)

    # --- Callback Queries: Navigation, Force-Sub Verification & YouTube Qualities ---
    @app.on_callback_query()
    async def callback_dispatcher(client: Client, query: CallbackQuery):
        data = query.data
        user_id = query.from_user.id
        if is_banned(user_id):
            return await query.answer("⛔ You are banned from using this bot!", show_alert=True)

        user_name = (query.from_user.first_name or "User").replace("<", "&lt;").replace(">", "&gt;")
        bot_info = getattr(client, "me", None) or await client.get_me()
        bot_username = bot_info.username or "Bot"
        bot_name = bot_info.first_name or "Media Downloader"

        # 1. Verification Callback
        if data.startswith("verify_"):
            try:
                target_uid = int(data.split("_")[1])
                if user_id != target_uid:
                    return await query.answer("⚠️ This button is not for you!", show_alert=True)
            except Exception:
                pass

            is_joined, updates_ok, deals_ok = await check_fsub(client, user_id)
            if not is_joined:
                missing = []
                if not updates_ok:
                    missing.append("📢 Updates Channel")
                if not deals_ok:
                    missing.append("🛍️ Loot Deals Channel")
                missing_str = " and ".join(missing)
                return await query.answer(
                    f"❌ Verification Failed!\n\nYou have NOT joined:\n👉 {missing_str}\n\nPlease join both channels and tap Verify again!",
                    show_alert=True
                )

            await query.answer("✅ Verification Successful! Welcome to the bot.", show_alert=True)
            try:
                if query.message.photo:
                    await query.message.edit_caption(
                        caption=Script.START_TXT.format(user_name),
                        reply_markup=get_start_buttons(bot_username),
                        parse_mode=enums.ParseMode.HTML
                    )
                else:
                    await query.message.delete()
                    await client.send_photo(
                        chat_id=query.message.chat.id,
                        photo=START_PIC,
                        caption=Script.START_TXT.format(user_name),
                        reply_markup=get_start_buttons(bot_username),
                        parse_mode=enums.ParseMode.HTML
                    )
            except Exception:
                pass
            return

        # 2. YouTube Quality Download Callback (ytq_{cache_id}_{idx})
        if data.startswith("ytq_"):
            parts = data.split("_")
            if len(parts) >= 3:
                cache_id = parts[1]
                idx = int(parts[2])

                cached = yt_cache.get(cache_id)
                if not cached:
                    return await query.answer("⚠️ Session Expired! Please re-send the YouTube link.", show_alert=True)

                download_links = cached.get("download_links", [])
                if idx >= len(download_links):
                    return await query.answer("⚠️ Invalid Quality selection.", show_alert=True)

                # Rate Limiting & Cooldown Check
                allowed, reason, rem = task_manager.check_user_allowed(user_id)
                if not allowed:
                    if reason == "running":
                        return await query.answer("⚠️ You already have an active task running! Please wait for it to complete.", show_alert=True)
                    elif reason == "cooldown":
                        return await query.answer(f"⏳ Cooldown active! Please wait {rem}s before starting a new task (1 min cooldown).", show_alert=True)

                task_manager.mark_user_active(user_id)

                selected = download_links[idx]
                video_url = selected.get("downloadUrl")
                audio_url = selected.get("audioUrl") or cached.get("best_audio_url")
                fmt = selected.get("format") or selected.get("label") or "best"
                itype = selected.get("type") or "video"
                title = cached.get("title") or "YouTube_Video"

                await query.answer(f"⏳ Processing {fmt}...", show_alert=False)

                status_msg = query.message
                safe_title = "".join(c for c in title if c.isalnum() or c in "._- ").strip() or "video"
                ts = int(time.time())
                task_start_time = time.time()

                raw_video_path = None
                raw_audio_path = None
                muxed_path = None
                mp3_path = None
                meta = {}

                try:
                    # Concurrency slot acquisition (Queue mode if 3 active)
                    queue_pos = await task_manager.acquire_slot(user_id, status_msg)
                    if queue_pos > 0:
                        await status_msg.edit_text(
                            f"⚡ <b>ǫᴜᴇᴜᴇ sʟᴏᴛ ɢʀᴀɴᴛᴇᴅ!</b>\n<i>sᴛᴀʀᴛɪɴɢ ʏᴏᴜʀ {fmt} ᴅᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ...</i>",
                            parse_mode=enums.ParseMode.HTML
                        )

                    # Log: New Task Added
                    queue_status_text = f"Queue #{queue_pos}" if queue_pos > 0 else "Active Slot (Immediate)"
                    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                    await send_log(
                        client,
                        Script.LOG_NEW_TASK_TXT.format(
                            user_id=user_id,
                            name=user_name,
                            provider=f"YouTube ({fmt.upper()})",
                            link_or_title=title,
                            queue_status=queue_status_text,
                            timestamp=now_str
                        )
                    )

                    if itype == "audio":
                        # Pure Audio Download
                        target_audio_url = video_url or audio_url
                        if not target_audio_url:
                            raise Exception("Audio stream URL not found.")

                        raw_audio_path = os.path.join(DOWNLOAD_DIR, f"{ts}_a_{safe_title}.m4a")
                        await status_msg.edit_text(
                            f"🎵 <b>Downloading Audio Stream:</b> <code>{title}</code>\n"
                            f"📦 <b>Format:</b> <code>{fmt.upper()}</code>\n"
                            f"<blockquote>⚡ <i>Connecting to high-speed stream from ytultra...</i></blockquote>"
                        )
                        audio_tracker = ProgressTracker(status_msg, f"🎵 Downloading Audio: {title}")
                        await download_file(target_audio_url, raw_audio_path, audio_tracker)

                        upload_file_path = raw_audio_path
                        file_name = f"{safe_title}_{fmt}.m4a"

                        # If user asked for MP3, convert AAC to MP3 with ffmpeg
                        if fmt.lower() == "mp3":
                            mp3_path = os.path.join(DOWNLOAD_DIR, f"{ts}_{safe_title}.mp3")
                            await status_msg.edit_text(
                                f"⚡ <b>Converting Audio to MP3 (192kbps)...</b>\n"
                                f"<blockquote>🎬 <i>Encoding with FFmpeg...</i></blockquote>"
                            )
                            if await convert_to_mp3_ffmpeg(raw_audio_path, mp3_path):
                                upload_file_path = mp3_path
                                file_name = f"{safe_title}.mp3"

                        file_size_bytes = os.path.getsize(upload_file_path)
                        file_size_human = format_size(file_size_bytes)
                        upload_tracker = ProgressTracker(status_msg, f"📤 Uploading Audio to Telegram: {title}")
                        async def upload_progress(current, total):
                            await upload_tracker.update(current, total)

                        caption = Script.CAPTION_TXT.format(
                            file_name=file_name,
                            file_size=file_size_human,
                            provider=f"YouTube ({fmt.upper()} Audio)",
                            deals_channel=DEALS_CHANNEL
                        )

                        await client.send_audio(
                            chat_id=query.message.chat.id,
                            audio=upload_file_path,
                            caption=caption,
                            title=title,
                            performer=cached.get("author") or "YouTube",
                            progress=upload_progress
                        )
                        db_log_download(user_id, "YouTube Audio", file_name, file_size_human)
                        await status_msg.delete()

                        # Log: Task Completed
                        elapsed_sec = int(time.time() - task_start_time)
                        dur_str = f"{elapsed_sec}s" if elapsed_sec < 60 else f"{elapsed_sec // 60}m {elapsed_sec % 60}s"
                        await send_log(
                            client,
                            Script.LOG_TASK_COMPLETED_TXT.format(
                                user_id=user_id,
                                name=user_name,
                                provider="YouTube (Audio)",
                                file_name=file_name,
                                file_size=file_size_human,
                                duration=dur_str,
                                timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                            )
                        )

                    else:
                        # Video Stream + Audio Muxing Workflow
                        v_ext = selected.get("ext") or "mp4"
                        raw_video_path = os.path.join(DOWNLOAD_DIR, f"{ts}_v_{safe_title}.{v_ext}")
                        muxed_path = os.path.join(DOWNLOAD_DIR, f"{ts}_{safe_title}_{fmt}.mp4")

                        # Step 1: Download Video Stream
                        await status_msg.edit_text(
                            f"⏬ <b>[1/3] Downloading Video Track:</b> <code>{title}</code>\n"
                            f"📦 <b>Quality:</b> <code>{fmt}</code>\n"
                            f"<blockquote>⚡ <i>Fetching adaptive video stream from ytultra...</i></blockquote>"
                        )
                        video_tracker = ProgressTracker(status_msg, f"⏬ [1/3] Video Track: {fmt}")
                        await download_file(video_url, raw_video_path, video_tracker)

                        # Step 2: Download Audio Stream if available
                        final_upload_path = raw_video_path
                        file_name = f"{safe_title}_{fmt}.{v_ext}"

                        if audio_url:
                            raw_audio_path = os.path.join(DOWNLOAD_DIR, f"{ts}_a_{safe_title}.m4a")
                            await status_msg.edit_text(
                                f"🎵 <b>[2/3] Downloading High-Quality Audio Track...</b>\n"
                                f"<blockquote>⚡ <i>Fetching synchronized audio stream...</i></blockquote>"
                            )
                            audio_tracker = ProgressTracker(status_msg, f"🎵 [2/3] Audio Track")
                            await download_file(audio_url, raw_audio_path, audio_tracker)

                            # Step 3: Fast Mux with FFmpeg
                            await status_msg.edit_text(
                                f"⚡ <b>[3/3] Fast Muxing Video + Audio via FFmpeg...</b>\n"
                                f"<blockquote>🎬 <i>Synchronizing media into single MP4 file...</i></blockquote>"
                            )
                            is_muxed = await mux_media_ffmpeg(raw_video_path, raw_audio_path, muxed_path)
                            if is_muxed:
                                final_upload_path = muxed_path
                                file_name = f"{safe_title}_{fmt}.mp4"

                        file_size_bytes = os.path.getsize(final_upload_path)
                        file_size_human = format_size(file_size_bytes)
                        upload_tracker = ProgressTracker(status_msg, f"📤 Uploading to Telegram via MTProto: {title}")
                        async def upload_progress(current, total):
                            await upload_tracker.update(current, total)

                        caption = Script.CAPTION_TXT.format(
                            file_name=file_name,
                            file_size=file_size_human,
                            provider=f"YouTube ({fmt} • ytultra Muxed)",
                            deals_channel=DEALS_CHANNEL
                        )

                        # Extract exact duration & thumbnail to avoid 00:00 bug
                        meta = await get_video_metadata(final_upload_path)

                        try:
                            await client.send_video(
                                chat_id=query.message.chat.id,
                                video=final_upload_path,
                                caption=caption,
                                duration=meta.get("duration") or 0,
                                width=meta.get("width") or 1280,
                                height=meta.get("height") or 720,
                                thumb=meta.get("thumb"),
                                supports_streaming=True,
                                progress=upload_progress
                            )
                        except Exception:
                            await client.send_document(
                                chat_id=query.message.chat.id,
                                document=final_upload_path,
                                caption=caption,
                                progress=upload_progress
                            )

                        db_log_download(user_id, "YouTube Video", file_name, file_size_human)
                        await status_msg.delete()

                        # Log: Task Completed
                        elapsed_sec = int(time.time() - task_start_time)
                        dur_str = f"{elapsed_sec}s" if elapsed_sec < 60 else f"{elapsed_sec // 60}m {elapsed_sec % 60}s"
                        await send_log(
                            client,
                            Script.LOG_TASK_COMPLETED_TXT.format(
                                user_id=user_id,
                                name=user_name,
                                provider=f"YouTube ({fmt})",
                                file_name=file_name,
                                file_size=file_size_human,
                                duration=dur_str,
                                timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                            )
                        )

                except Exception as e:
                    await status_msg.edit_text(
                        f"❌ <b>Download Error:</b> <code>{str(e)}</code>\n\n"
                        f"🔗 <b>Direct Video Link:</b> <a href='{video_url}'>Click here</a>"
                    )
                finally:
                    # Clean up all temp files
                    for p in [raw_video_path, raw_audio_path, muxed_path, mp3_path]:
                        if p and os.path.exists(p):
                            try:
                                os.remove(p)
                            except Exception:
                                pass
                    if meta and meta.get("thumb") and os.path.exists(meta["thumb"]):
                        try:
                            os.remove(meta["thumb"])
                        except Exception:
                            pass
                    await task_manager.release_slot(user_id)
            return

        # 3. Menu Navigation
        if data == "home":
            try:
                if query.message.photo:
                    await query.message.edit_caption(
                        caption=Script.START_TXT.format(user_name),
                        reply_markup=get_start_buttons(bot_username),
                        parse_mode=enums.ParseMode.HTML
                    )
                else:
                    await query.message.delete()
                    await client.send_photo(
                        chat_id=query.message.chat.id,
                        photo=START_PIC,
                        caption=Script.START_TXT.format(user_name),
                        reply_markup=get_start_buttons(bot_username),
                        parse_mode=enums.ParseMode.HTML
                    )
            except Exception:
                pass

        elif data == "help":
            try:
                if query.message.photo:
                    await query.message.edit_caption(
                        caption=Script.HELP_TXT.format(SUPPORT_CHAT),
                        reply_markup=get_help_buttons(),
                        parse_mode=enums.ParseMode.HTML
                    )
                else:
                    await query.message.edit_text(
                        text=Script.HELP_TXT.format(SUPPORT_CHAT),
                        reply_markup=get_help_buttons(),
                        disable_web_page_preview=True,
                        parse_mode=enums.ParseMode.HTML
                    )
            except Exception:
                pass

        elif data == "about":
            try:
                if query.message.photo:
                    await query.message.edit_caption(
                        caption=Script.ABOUT_TXT.format(bot_username, bot_name),
                        reply_markup=get_about_buttons(),
                        parse_mode=enums.ParseMode.HTML
                    )
                else:
                    await query.message.edit_text(
                        text=Script.ABOUT_TXT.format(bot_username, bot_name),
                        reply_markup=get_about_buttons(),
                        disable_web_page_preview=True,
                        parse_mode=enums.ParseMode.HTML
                    )
            except Exception:
                pass

        elif data == "close":
            try:
                await query.message.delete()
            except Exception:
                pass

    # --- Message Handler: TeraBox, Diskwala & YouTube Link Processing ---
    @app.on_message(filters.text & filters.private & ~filters.command(["start", "help", "about", "ping", "ban", "unban", "addsudo", "delsudo", "sudolist", "admins", "banlist", "banned", "stats"]))
    async def text_link_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if is_banned(user_id):
            return await message.reply_text(
                Script.USER_BANNED_ALERT_TXT,
                parse_mode=enums.ParseMode.HTML
            )

        user_name = message.from_user.first_name or "User"

        # 1. Enforce Force-Sub on link processing
        is_joined, _, _ = await check_fsub(client, user_id)
        if not is_joined:
            updates_link = await get_channel_invite(client, UPDATES_CHANNEL)
            deals_link = await get_channel_invite(client, DEALS_CHANNEL)
            buttons = get_fsub_buttons(updates_link, deals_link, user_id)
            return await message.reply_text(
                text=Script.FORCE_SUB_TXT.format(user_name),
                reply_markup=buttons,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )

        urls = extract_urls(message.text)
        if not urls:
            return

        for url in urls:
            link_type = detect_link_type(url)
            if not link_type:
                continue

            # --- CASE A: YouTube Video Link ---
            if link_type == "youtube":
                status_msg = await message.reply_text(
                    Script.YT_WAIT_TXT,
                    parse_mode=enums.ParseMode.HTML
                )
                try:
                    yt_info = await resolve_youtube(url)
                    cache_id = f"yt_{int(time.time())}_{user_id}"
                    yt_cache[cache_id] = {
                        "title": yt_info["title"],
                        "author": yt_info["author"],
                        "thumbnail": yt_info.get("thumbnail"),
                        "download_links": yt_info["download_links"],
                        "user_id": user_id
                    }

                    buttons = get_youtube_quality_buttons(cache_id, yt_info["download_links"])
                    info_text = Script.YT_INFO_TXT.format(
                        title=yt_info["title"],
                        author=yt_info["author"]
                    )
                    await status_msg.edit_text(
                        text=info_text,
                        reply_markup=buttons,
                        parse_mode=enums.ParseMode.HTML,
                        disable_web_page_preview=True
                    )
                except Exception as e:
                    await status_msg.edit_text(
                        f"❌ <b>YouTube Extraction Failed:</b>\n<code>{str(e)}</code>\n\n"
                        "Tip: Verify the YouTube link is publicly available."
                    )
                continue

            # --- CASE B: TeraBox & Diskwala Direct Resolvers ---
            # Rate Limiting & Cooldown Check (1 Task per user, 1-min cooldown)
            allowed, reason, rem = task_manager.check_user_allowed(user_id)
            if not allowed:
                if reason == "running":
                    await message.reply_text(
                        Script.TASK_ALREADY_RUNNING_TXT.format(user_name),
                        parse_mode=enums.ParseMode.HTML
                    )
                elif reason == "cooldown":
                    await message.reply_text(
                        Script.TASK_COOLDOWN_TXT.format(user_name, rem),
                        parse_mode=enums.ParseMode.HTML
                    )
                continue

            task_manager.mark_user_active(user_id)
            status_msg = await message.reply_text(f"🔍 <i>Detecting & resolving {link_type.upper()} link via Sunil-SSBots API...</i>")
            tmp_path = None
            meta = {}
            task_start_time = time.time()

            try:
                # Concurrency slot acquisition (Queue mode if 3 active tasks)
                queue_pos = await task_manager.acquire_slot(user_id, status_msg)
                if queue_pos > 0:
                    await status_msg.edit_text(
                        f"⚡ <b>ǫᴜᴇᴜᴇ sʟᴏᴛ ɢʀᴀɴᴛᴇᴅ!</b>\n<i>sᴛᴀʀᴛɪɴɢ ʏᴏᴜʀ {link_type.upper()} ᴅᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ...</i>",
                        parse_mode=enums.ParseMode.HTML
                    )

                # Log: New Task Added
                queue_status_text = f"Queue #{queue_pos}" if queue_pos > 0 else "Active Slot (Immediate)"
                now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                await send_log(
                    client,
                    Script.LOG_NEW_TASK_TXT.format(
                        user_id=user_id,
                        name=user_name,
                        provider=link_type.upper(),
                        link_or_title=url,
                        queue_status=queue_status_text,
                        timestamp=now_str
                    )
                )

                if link_type == "terabox":
                    info = await resolve_terabox(url)
                elif link_type == "diskwala":
                    info = await resolve_diskwala(url)
                else:
                    await status_msg.edit_text("❌ Unsupported link format.")
                    continue

                file_name = info["name"]
                file_size = info["size"]
                dlink = info["dlink"]

                # Check max size limit
                size_mb = (info.get("size_bytes") or 0) / (1024 * 1024)
                if size_mb > MAX_FILE_SIZE_MB:
                    await status_msg.edit_text(
                        f"⚠️ <b>File exceeds limit:</b> {file_name} ({file_size})\n"
                        f"Maximum upload limit is {MAX_FILE_SIZE_MB} MB.\n\n"
                        f"🔗 <b>Direct Link:</b> <a href='{dlink}'>Click to Download</a>"
                    )
                    continue

                safe_name = "".join(c for c in file_name if c.isalnum() or c in "._- ").strip() or "file.mp4"
                tmp_path = os.path.join(DOWNLOAD_DIR, f"{int(time.time())}_{safe_name}")

                download_tracker = ProgressTracker(status_msg, f"⏬ Downloading: {file_name} ({file_size})")
                await download_file(dlink, tmp_path, download_tracker)

                upload_tracker = ProgressTracker(status_msg, f"📤 Uploading via MTProto: {file_name}")

                async def upload_progress(current, total):
                    await upload_tracker.update(current, total)

                caption = Script.CAPTION_TXT.format(
                    file_name=file_name,
                    file_size=file_size,
                    provider=info["provider"],
                    deals_channel=DEALS_CHANNEL
                )

                ext = file_name.split(".")[-1].lower() if "." in file_name else ""
                if ext in ["mp4", "mkv", "webm", "mov", "avi"]:
                    # Fix TeraBox 00:00 duration bug and generate video thumbnail
                    await status_msg.edit_text(
                        f"⚡ <b>ᴇxᴛʀᴀᴄᴛɪɴɢ ᴠɪᴅᴇᴏ ᴅᴜʀᴀᴛɪᴏɴ & ᴛʜᴜᴍʙɴᴀɪʟ...</b>\n"
                        f"<blockquote>🎬 <i>ᴀɴᴀʟʏᴢɪɴɢ ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍ ʜᴇᴀᴅᴇʀs ᴠɪᴀ ғғᴍᴘᴇɢ...</i></blockquote>",
                        parse_mode=enums.ParseMode.HTML
                    )
                    meta = await get_video_metadata(tmp_path)
                    try:
                        await client.send_video(
                            chat_id=message.chat.id,
                            video=tmp_path,
                            caption=caption,
                            duration=meta.get("duration") or 0,
                            width=meta.get("width") or 1280,
                            height=meta.get("height") or 720,
                            thumb=meta.get("thumb"),
                            progress=upload_progress,
                            supports_streaming=True
                        )
                    except Exception:
                        await client.send_document(
                            chat_id=message.chat.id,
                            document=tmp_path,
                            caption=caption,
                            progress=upload_progress
                        )
                else:
                    await client.send_document(
                        chat_id=message.chat.id,
                        document=tmp_path,
                        caption=caption,
                        progress=upload_progress
                    )

                db_log_download(user_id, link_type.upper(), file_name, file_size)
                await status_msg.delete()

                # Log: Task Completed
                elapsed_sec = int(time.time() - task_start_time)
                dur_str = f"{elapsed_sec}s" if elapsed_sec < 60 else f"{elapsed_sec // 60}m {elapsed_sec % 60}s"
                now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                await send_log(
                    client,
                    Script.LOG_TASK_COMPLETED_TXT.format(
                        user_id=user_id,
                        name=user_name,
                        provider=link_type.upper(),
                        file_name=file_name,
                        file_size=file_size,
                        duration=dur_str,
                        timestamp=now_str
                    )
                )

            except Exception as e:
                await status_msg.edit_text(
                    f"❌ <b>Error:</b> <code>{str(e)}</code>\n\n"
                    "Tip: Make sure the link is public and still accessible."
                )
            finally:
                if meta and meta.get("thumb") and os.path.exists(meta["thumb"]):
                    try:
                        os.remove(meta["thumb"])
                    except Exception:
                        pass
                if tmp_path and os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except Exception:
                        pass
                await task_manager.release_slot(user_id)

async def main_runner():
    """Startup runner for Pyrogram MTProto bot."""
    await app.start()
    await log_bot_started(app)
    from pyrogram import idle
    await idle()
    await app.stop()

def run():
    if not app:
        print("[ERROR] Please configure API_ID, API_HASH, and BOT_TOKEN in .env file!")
        sys.exit(1)

    deploy_banner = (
        "====================================================================\n"
        f"🚀 TERA BOX, DISKWALA & YOUTUBE BOT DEPLOYED SUCCESSFULLY!\n"
        f"👤 Developer / Owner: {DEVELOPER_NAME} ({DEVELOPER_URL})\n"
        f"📢 Telegram Channel : {CHANNEL_URL} (@{UPDATES_CHANNEL})\n"
        f"📺 YouTube Channel  : {YOUTUBE_URL} (SunilWebTricks)\n"
        f"💬 Ask Doubt/Support: @{SUPPORT_CHAT}\n"
        f"📢 Log Channel      : {LOG_CHANNEL}\n"
        f"🛡️ Sudo Admins      : {list(sudo_users_set)}\n"
        f"🌐 TeraBox API     : {TERABOX_API_URL}\n"
        f"🌐 Diskwala API    : {DISKWALA_API_URL}\n"
        f"🌐 YouTube API     : {YOUTUBE_API_URL}\n"
        "===================================================================="
    )
    print(deploy_banner)

    try:
        app.run(main_runner())
    except Exception as e:
        print(f"Bot execution error: {e}")

if __name__ == "__main__":
    run()
