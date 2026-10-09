#!/usr/bin/env python3
# ==============================================================================
# 🤖 Bot Developer / Owner : Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ
# 🌐 Developer URL        : https://t.me/Sunil_Sharma_2_0_Bot (@Sunil_Sharma_2_0_Bot)
# 📢 Telegram Channel     : https://t.me/SSBotsUpdates (@SSBotsUpdates)
# 📺 YouTube Channel      : https://www.youtube.com/@SunilWebTricks (SunilWebTricks)
# 💬 Ask Doubt / Contact   : @Sunil_Sharma_2_0_Bot
# ==============================================================================

"""
🚀 TeraBox, Diskwala & YouTube Downloader Bot (Modular Architecture)
- Automated Bot Command Menu Registration on Start (set_bot_commands)
- Pyrogram MTProto 2GB Upload Support
- Dual Channel Force-Subscribe Check (@SSBotsUpdates & @Tg_Shoping)
- Powered by Sunil-SSBots Custom Engine (https://sunil-ssbots.vercel.app)
"""

import os
import sys
import shutil
import asyncio

# Ensure project root is prioritized in sys.path
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

import config
from core.client import app, setup_bot_commands
from handlers import register_all_handlers
from helpers.logger import log_bot_started
from database.db import sudo_users_set, db

async def main_runner():
    """Startup runner for Pyrogram MTProto bot."""
    await app.start()
    
    # 1. Automatically register all bot commands on Telegram menu!
    await setup_bot_commands(app)
    
    # 2. Dispatch bot started alert to LOG_CHANNEL
    await log_bot_started(app)
    
    from pyrogram import idle
    await idle()
    await app.stop()

def run():
    if not app:
        print("[ERROR] Please configure API_ID, API_HASH, and BOT_TOKEN in .env file!")
        sys.exit(1)

    # Register modular handlers (commands, callbacks, media)
    register_all_handlers(app)

    db_status = "Connected (MongoDB)" if db is not None else "In-Memory Active"
    deploy_banner = (
        "====================================================================\n"
        "🚀 TERA BOX, DISKWALA & YOUTUBE BOT INITIALIZED SUCCESSFULLY!\n"
        f"👤 Developer / Owner: {getattr(config, 'DEVELOPER_NAME', 'Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ')}\n"
        f"📢 Telegram Channel : {getattr(config, 'CHANNEL_URL', 'https://t.me/SSBotsUpdates')}\n"
        f"📺 YouTube Channel  : {getattr(config, 'YOUTUBE_URL', 'https://www.youtube.com/@SunilWebTricks')}\n"
        f"💬 Support Chat     : @{getattr(config, 'SUPPORT_CHAT', 'Sunil_Sharma_2_0_Bot')}\n"
        f"📢 Log Channel      : {getattr(config, 'LOG_CHANNEL', 'Not Configured')}\n"
        f"🗄️ Database         : {db_status}\n"
        f"🛡️ Sudo Admins      : {list(sudo_users_set)}\n"
        "✨ Commands Status   : Automatically Registered on Telegram Menu\n"
        "===================================================================="
    )
    print(deploy_banner)

    try:
        app.run(main_runner())
    except Exception as e:
        print(f"[FATAL] Bot runtime error: {e}")

if __name__ == "__main__":
    run()
