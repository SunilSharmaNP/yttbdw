# ==============================================================================
# 🤖 Bot Developer / Owner : Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ
# 🌐 Developer URL        : https://t.me/Sunil_Sharma_2_0_Bot (@Sunil_Sharma_2_0_Bot)
# 📢 Telegram Channel     : https://t.me/SSBotsUpdates (@SSBotsUpdates)
# 📺 YouTube Channel      : https://www.youtube.com/@SunilWebTricks (SunilWebTricks)
# 💬 Ask Doubt / Contact   : @Sunil_Sharma_2_0_Bot
# ==============================================================================

import os
import sys

# Safely load .env if python-dotenv is present (Heroku uses os.environ directly)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def _clean_str(val, default: str = "") -> str:
    """Cleans quotes, leading/trailing whitespace from string env vars"""
    if val is None:
        return default
    s = str(val).strip().strip("\"'").strip()
    return s if s else default

def _clean_int(val, default: int = 0) -> int:
    """Safely parses integers even if enclosed in quotes or with whitespace"""
    if val is None:
        return default
    s = str(val).strip().strip("\"'").strip()
    try:
        return int(s)
    except (ValueError, TypeError):
        return default

def _clean_channel(ch, default: str = "") -> str:
    """Normalizes channel username or ID from URL, @, or raw ID"""
    s = _clean_str(ch, default)
    if not s:
        return default
    if s.startswith("-100") or s.lstrip("-").isdigit():
        return s
    for prefix in ["https://t.me/", "http://t.me/", "t.me/", "tg://resolve?domain="]:
        if s.startswith(prefix):
            s = s[len(prefix):]
    return s.lstrip("@").strip()

# --- Developer & Branding Info ---
DEVELOPER_NAME = "Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ"
DEVELOPER_URL = "https://t.me/Sunil_Sharma_2_0_Bot"
CHANNEL_URL = "https://t.me/SSBotsUpdates"
YOUTUBE_URL = "https://www.youtube.com/@SunilWebTricks"
SUPPORT_CHAT = "Sunil_Sharma_2_0_Bot"

# --- Telegram Credentials ---
API_ID = _clean_int(os.getenv("API_ID"), 0)
API_HASH = _clean_str(os.getenv("API_HASH"), "")
BOT_TOKEN = _clean_str(os.getenv("BOT_TOKEN"), "")
SESSION_STRING = _clean_str(os.getenv("SESSION_STRING"), "")

# --- Owner Info ---
OWNER_ID = _clean_int(os.getenv("OWNER_ID"), 2032446867)
OWNER_USERNAME = _clean_channel(os.getenv("OWNER_USERNAME"), "Sunil_Sharma_2_0_Bot")

# --- Mandatory 2 Force Subscribe Channels ---
UPDATES_CHANNEL = _clean_channel(os.getenv("UPDATES_CHANNEL"), "SSBotsUpdates")
DEALS_CHANNEL = _clean_channel(os.getenv("DEALS_CHANNEL"), "Tg_Shoping")

# --- Optional Log Channel ---
_raw_log = _clean_str(os.getenv("LOG_CHANNEL"), "")
if _raw_log:
    LOG_CHANNEL = _clean_int(_raw_log, 0)
    if LOG_CHANNEL == 0:
        LOG_CHANNEL = None
else:
    LOG_CHANNEL = None

# --- Custom High-Speed API Endpoints (Sunil-SSBots Engine) ---
TERABOX_API_URL = _clean_str(os.getenv("TERABOX_API_URL"), "https://sunil-ssbots.vercel.app/api/terabox")
DISKWALA_API_URL = _clean_str(os.getenv("DISKWALA_API_URL"), "https://sunil-ssbots.vercel.app/api/diskwala")
YOUTUBE_API_URL = _clean_str(os.getenv("YOUTUBE_API_URL"), "https://sunil-ssbots.vercel.app/api/youtube")

# --- Optional TeraBox Cookies ---
TERABOX_COOKIES = _clean_str(os.getenv("TERABOX_COOKIES"), "")

# --- Download & Upload Settings ---
DOWNLOAD_DIR = _clean_str(os.getenv("DOWNLOAD_DIR"), "./downloads")
try:
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
except Exception:
    pass

# 2GB upload limit (standard MTProto: 2048 MB)
MAX_FILE_SIZE_MB = _clean_int(os.getenv("MAX_FILE_SIZE_MB"), 2048)

# Class-based alias for compatibility with different import styles
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
    UPDATES_CHANNEL = UPDATES_CHANNEL
    DEALS_CHANNEL = DEALS_CHANNEL
    LOG_CHANNEL = LOG_CHANNEL
    TERABOX_API_URL = TERABOX_API_URL
    DISKWALA_API_URL = DISKWALA_API_URL
    YOUTUBE_API_URL = YOUTUBE_API_URL
    TERABOX_COOKIES = TERABOX_COOKIES
    DOWNLOAD_DIR = DOWNLOAD_DIR
    MAX_FILE_SIZE_MB = MAX_FILE_SIZE_MB

Telegram = Config
