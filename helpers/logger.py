import asyncio
from datetime import datetime
from pyrogram import Client, enums
from pyrogram.errors import FloodWait
import config
from translations import Script
from database.db import db

LOG_CHANNEL = getattr(config, "LOG_CHANNEL", None)
OWNER_ID = getattr(config, "OWNER_ID", 2032446867)
MAX_CONCURRENT_TASKS = getattr(config, "MAX_CONCURRENT_TASKS", 3)
USER_COOLDOWN_SECONDS = getattr(config, "USER_COOLDOWN_SECONDS", 60)

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
        err_msg = str(e)
        if "Peer id invalid" in err_msg or "PEER_ID_INVALID" in err_msg:
            print(f"[LOG CHANNEL NOTE] Peer id invalid ({LOG_CHANNEL}): Bot must be added as an ADMINISTRATOR in your Log Channel to send logs.")
        else:
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
