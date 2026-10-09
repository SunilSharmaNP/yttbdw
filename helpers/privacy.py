import os
import time
import asyncio
from pyrogram import Client
from pyrogram.types import Message
import config
from database.db import get_user_thumbnail

DOWNLOAD_DIR = getattr(config, "DOWNLOAD_DIR", "./downloads")

async def auto_delete_message(client: Client, chat_id: int, message_id: int, delay_seconds: int = 600):
    """
    Schedules auto-deletion of a message (e.g. copyright links sent by user)
    after specified duration (default: 10 minutes = 600s).
    Protects user & bot privacy and complies with copyright safe-harbor.
    """
    try:
        await asyncio.sleep(delay_seconds)
        await client.delete_messages(chat_id=chat_id, message_ids=message_id)
        print(f"[PRIVACY] Auto-deleted message {message_id} in chat {chat_id} after {delay_seconds}s.")
    except Exception as e:
        # Chat might be deleted or message already gone
        pass

async def get_effective_thumbnail(client: Client, user_id: int, default_thumb: str = None) -> str | None:
    """
    Checks if the user has saved a custom thumbnail via /setthumb.
    If so, downloads it to local disk and returns path.
    Otherwise falls back to default_thumb (FFmpeg snapshot).
    """
    thumb_file_id = get_user_thumbnail(user_id)
    if thumb_file_id:
        try:
            custom_path = os.path.join(DOWNLOAD_DIR, f"custom_thumb_{user_id}_{int(time.time())}.jpg")
            downloaded = await client.download_media(thumb_file_id, file_name=custom_path)
            if downloaded and os.path.exists(downloaded):
                return downloaded
        except Exception as e:
            print(f"[CUSTOM THUMB NOTE] Failed to fetch custom thumb: {e}")

    return default_thumb
