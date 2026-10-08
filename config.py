# ==============================================================================
# 🤖 Bot Developer / Owner : Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ
# 🌐 Developer URL        : https://t.me/Sunil_Sharma_2_0_Bot (@Sunil_Sharma_2_0_Bot)
# 📢 Telegram Channel     : https://t.me/SSBotsUpdates (@SSBotsUpdates)
# 📺 YouTube Channel      : https://www.youtube.com/@SunilWebTricks (SunilWebTricks)
# 💬 Ask Doubt / Contact   : @Sunil_Sharma_2_0_Bot
# ==============================================================================

import os
from dotenv import load_dotenv

load_dotenv()

# --- Developer & Branding Info ---
DEVELOPER_NAME = "Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ"
DEVELOPER_URL = "https://t.me/Sunil_Sharma_2_0_Bot"
CHANNEL_URL = "https://t.me/SSBotsUpdates"
YOUTUBE_URL = "https://www.youtube.com/@SunilWebTricks"
SUPPORT_CHAT = "Sunil_Sharma_2_0_Bot"

# --- Telegram Credentials ---
API_ID = int(os.getenv("API_ID", "0") or "0")
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")

# --- Owner Info ---
OWNER_ID = int(os.getenv("OWNER_ID", "2032446867") or "2032446867")
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "Sunil_Sharma_2_0_Bot").lstrip("@")

# --- Mandatory 2 Force Subscribe Channels ---
UPDATES_CHANNEL = os.getenv("UPDATES_CHANNEL", "SSBotsUpdates").lstrip("@")
DEALS_CHANNEL = os.getenv("DEALS_CHANNEL", "Tg_Shoping").lstrip("@")

# --- Optional Log Channel ---
LOG_CHANNEL = os.getenv("LOG_CHANNEL", "")
try:
    LOG_CHANNEL = int(LOG_CHANNEL) if LOG_CHANNEL else None
except ValueError:
    LOG_CHANNEL = None

# --- TeraBox & Diskwala Settings ---
TERABOX_COOKIES = os.getenv("TERABOX_COOKIES", "")
COOKIE_POOL_URL = os.getenv("TERABOX_COOKIE_POOL_URL", "https://tera.backend.live/cookies-list")
DISKWALA_RESOLVER_URL = os.getenv("DISKWALA_RESOLVER_URL", "https://diskwala-dl-six.vercel.app/api/scrap")

# --- Download & Upload Settings ---
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 2GB upload limit (standard MTProto)
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "2048"))
