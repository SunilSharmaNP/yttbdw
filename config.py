# ==============================================================================
# 🤖 Bot Developer / Owner : Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ
# 🌐 Developer URL        : https://t.me/Sunil_Sharma_2_0_Bot (@Sunil_Sharma_2_0_Bot)
# 📢 Telegram Channel     : https://t.me/SSBotsUpdates (@SSBotsUpdates)
# 📺 YouTube Channel      : https://www.youtube.com/@SunilWebTricks (SunilWebTricks)
# 💬 Support Chat         : @Sunil_Sharma_2_0_Bot
# ==============================================================================

import os
import sys
import re

# Safely load .env if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def _clean_str(val, default: str = "") -> str:
    """Cleans quotes, leading/trailing whitespace from string env vars."""
    if val is None:
        return default
    s = str(val).strip().strip("\"'").strip()
    return s if s else default

def _clean_int(val, default: int = 0) -> int:
    """Safely parses integers even if enclosed in quotes or with whitespace."""
    if val is None:
        return default
    s = str(val).strip().strip("\"'").strip()
    try:
        return int(s)
    except (ValueError, TypeError):
        return default

def _clean_id_list(val, default=None) -> list[int]:
    """Safely parses comma-separated or space-separated user IDs into a list of ints."""
    if default is None:
        default = []
    if not val:
        return default
    result = []
    parts = re.split(r'[,;\s]+', str(val).strip().strip("\"'").strip())
    for p in parts:
        p = p.strip()
        if p and (p.isdigit() or (p.startswith('-') and p[1:].isdigit())):
            try:
                val_int = int(p)
                if val_int not in result:
                    result.append(val_int)
            except ValueError:
                pass
    return result if result else default

def _clean_log_channel(val):
    """Normalizes log channel ID (e.g. -1001234567890) or username (e.g. @SSBotsLogs)."""
    if not val:
        return None
    s = str(val).strip().strip("\"'").strip()
    if not s:
        return None
    try:
        return int(s)
    except ValueError:
        for prefix in ["https://t.me/", "http://t.me/", "t.me/"]:
            if s.startswith(prefix):
                s = s[len(prefix):]
        s = s.lstrip("@").strip()
        return f"@{s}" if s else None

def _clean_channel(ch, default: str = "") -> str:
    """Normalizes channel username or ID from URL, @ prefix, or raw numeric ID."""
    s = _clean_str(ch, default)
    if not s:
        return default
    if s.startswith("-100") or s.lstrip("-").isdigit():
        return s
    for prefix in ["https://t.me/", "http://t.me/", "t.me/", "tg://resolve?domain="]:
        if s.startswith(prefix):
            s = s[len(prefix):]
    return s.lstrip("@").strip()

# ==============================================================================
# 1. Developer & Branding Constants
# ==============================================================================
DEVELOPER_NAME = "Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ"
DEVELOPER_URL = "https://t.me/Sunil_Sharma_2_0_Bot"
CHANNEL_URL = "https://t.me/SSBotsUpdates"
YOUTUBE_URL = "https://www.youtube.com/@SunilWebTricks"
SUPPORT_CHAT = "Sunil_Sharma_2_0_Bot"

# ==============================================================================
# 2. Telegram API Credentials
# ==============================================================================
API_ID = _clean_int(os.getenv("API_ID"), 0)
API_HASH = _clean_str(os.getenv("API_HASH"), "")
BOT_TOKEN = _clean_str(os.getenv("BOT_TOKEN"), "")
SESSION_STRING = _clean_str(os.getenv("SESSION_STRING"), "")

# ==============================================================================
# 3. Owner & Administrator Settings
# ==============================================================================
OWNER_ID = _clean_int(os.getenv("OWNER_ID"), 2032446867)
OWNER_USERNAME = _clean_channel(os.getenv("OWNER_USERNAME"), "Sunil_Sharma_2_0_Bot")
_raw_sudo = os.getenv("SUDO_USERS", "")
SUDO_USERS = _clean_id_list(_raw_sudo, [OWNER_ID])
if OWNER_ID not in SUDO_USERS:
    SUDO_USERS.append(OWNER_ID)

# ==============================================================================
# 4. Mandatory Force-Subscribe Channels (Dual Verification)
# ==============================================================================
UPDATES_CHANNEL = _clean_channel(os.getenv("UPDATES_CHANNEL"), "SSBotsUpdates")
DEALS_CHANNEL = _clean_channel(os.getenv("DEALS_CHANNEL"), "Tg_Shoping")

# ==============================================================================
# 5. Logging & Monitoring Channel
# ==============================================================================
LOG_CHANNEL = _clean_log_channel(os.getenv("LOG_CHANNEL"))

# ==============================================================================
# 6. UI Banner & Start Photo Settings
# ==============================================================================
START_PIC = _clean_str(
    os.getenv("START_PIC"),
    "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1200&auto=format&fit=crop"
)

# ==============================================================================
# 7. Task Queue & Concurrency Limits
# ==============================================================================
MAX_CONCURRENT_TASKS = _clean_int(os.getenv("MAX_CONCURRENT_TASKS"), 3)
USER_COOLDOWN_SECONDS = _clean_int(os.getenv("USER_COOLDOWN_SECONDS"), 60)

# ==============================================================================
# 8. High-Speed Media Resolver API Endpoints
# ==============================================================================
TERABOX_API_URL = _clean_str(os.getenv("TERABOX_API_URL"), "https://sunil-ssbots.vercel.app/api/terabox")
DISKWALA_API_URL = _clean_str(os.getenv("DISKWALA_API_URL"), "https://sunil-ssbots.vercel.app/api/diskwala")
YOUTUBE_API_URL = _clean_str(os.getenv("YOUTUBE_API_URL"), "https://sunil-ssbots.vercel.app/api/youtube")
YTULTRA_API_URL = _clean_str(os.getenv("YTULTRA_API_URL"), "https://api.ytultra.com/ikool/youtube/download")

# ==============================================================================
# 9. Storage, Download & Upload Limits
# ==============================================================================
DOWNLOAD_DIR = _clean_str(os.getenv("DOWNLOAD_DIR"), "./downloads")
try:
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
except Exception:
    pass

MAX_FILE_SIZE_MB = _clean_int(os.getenv("MAX_FILE_SIZE_MB"), 2048)
TERABOX_COOKIES = _clean_str(os.getenv("TERABOX_COOKIES"), "")

# ==============================================================================
# 10. Database Configuration (MongoDB)
# ==============================================================================
MONGO_URI = _clean_str(os.getenv("MONGO_URI"), "")
DATABASE_NAME = _clean_str(os.getenv("DATABASE_NAME"), "ss_downloader_bot")

# ==============================================================================
# 11. Server & AI Studio Runtime Config
# ==============================================================================
PORT = _clean_int(os.getenv("PORT"), 3000)
GEMINI_API_KEY = _clean_str(os.getenv("GEMINI_API_KEY"), "")

# ==============================================================================
# Class-based Alias Container (Supports multiple import paradigms)
# ==============================================================================
class Config:
    DEVELOPER_NAME = DEVELOPER_NAME
    DEVELOPER_URL = DEVELOPER_URL
    CHANNEL_URL = CHANNEL_URL
    YOUTUBE_URL = YOUTUBE_URL
    SUPPORT_CHAT = SUPPORT_CHAT
    API_ID = API_ID
    API_HASH = API_HASH
    BOT_TOKEN = BOT_TOKEN
    SESSION_STRING = SESSION_STRING
    OWNER_ID = OWNER_ID
    OWNER_USERNAME = OWNER_USERNAME
    SUDO_USERS = SUDO_USERS
    UPDATES_CHANNEL = UPDATES_CHANNEL
    DEALS_CHANNEL = DEALS_CHANNEL
    LOG_CHANNEL = LOG_CHANNEL
    START_PIC = START_PIC
    MAX_CONCURRENT_TASKS = MAX_CONCURRENT_TASKS
    USER_COOLDOWN_SECONDS = USER_COOLDOWN_SECONDS
    TERABOX_API_URL = TERABOX_API_URL
    DISKWALA_API_URL = DISKWALA_API_URL
    YOUTUBE_API_URL = YOUTUBE_API_URL
    YTULTRA_API_URL = YTULTRA_API_URL
    DOWNLOAD_DIR = DOWNLOAD_DIR
    MAX_FILE_SIZE_MB = MAX_FILE_SIZE_MB
    TERABOX_COOKIES = TERABOX_COOKIES
    MONGO_URI = MONGO_URI
    DATABASE_NAME = DATABASE_NAME
    PORT = PORT
    GEMINI_API_KEY = GEMINI_API_KEY

Telegram = Config
