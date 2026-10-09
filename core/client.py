import os
import sys
from pyrogram import Client
from pyrogram.types import BotCommand, BotCommandScopeDefault
import config

API_ID = getattr(config, "API_ID", 0)
API_HASH = getattr(config, "API_HASH", "")
BOT_TOKEN = getattr(config, "BOT_TOKEN", "")
SESSION_STRING = getattr(config, "SESSION_STRING", "")

app = None

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
    print("[WARNING] API_ID/API_HASH and BOT_TOKEN or SESSION_STRING not set in .env")

async def setup_bot_commands(client: Client):
    """
    Automatically registers all bot commands into Telegram so users see
    the autocomplete command menu with descriptions whenever they type '/'.
    """
    if not client:
        return
    commands = [
        BotCommand("start", "🚀 Start the bot & show main menu"),
        BotCommand("help", "📖 How to download videos & audio"),
        BotCommand("about", "ℹ️ Bot info, developer & channels"),
        BotCommand("ping", "🏓 Check bot latency & status"),
        BotCommand("setthumb", "🖼️ Set custom video thumbnail"),
        BotCommand("viewthumb", "👁️ View saved custom thumbnail"),
        BotCommand("delthumb", "🗑️ Delete custom thumbnail"),
        BotCommand("stats", "📊 View bot & system stats (Admins)"),
        BotCommand("broadcast", "📢 Broadcast announcement to all users (Admins)"),
        BotCommand("sudolist", "🛡️ View list of sudo administrators"),
        BotCommand("banlist", "🚫 View list of banned users (Admins)"),
    ]
    try:
        await client.set_bot_commands(commands, scope=BotCommandScopeDefault())
        print("✅ [AUTO-COMMANDS] Successfully registered bot commands on Telegram!")
    except Exception as e:
        print(f"⚠️ [AUTO-COMMANDS NOTE] Could not set bot commands: {e}")
