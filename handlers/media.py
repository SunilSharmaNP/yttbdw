import os
import time
import asyncio
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import Message
import config
from translations import (
    Script,
    get_fsub_buttons,
    get_youtube_quality_buttons,
)
from database.db import (
    is_banned,
    db_log_download,
)
from helpers.fsub import check_fsub, get_channel_invite
from helpers.logger import send_log
from helpers.cache import yt_cache
from helpers.progress import ProgressTracker, download_file, get_cancel_button
from helpers.ffmpeg import get_video_metadata
from helpers.privacy import auto_delete_message, get_effective_thumbnail
from core.queue import task_manager, TaskCancelledException
from resolvers import (
    extract_urls,
    detect_link_type,
    resolve_terabox,
    resolve_diskwala,
    resolve_youtube,
)

UPDATES_CHANNEL = getattr(config, "UPDATES_CHANNEL", "SSBotsUpdates")
DEALS_CHANNEL = getattr(config, "DEALS_CHANNEL", "Tg_Shoping")
DOWNLOAD_DIR = getattr(config, "DOWNLOAD_DIR", "./downloads")
MAX_FILE_SIZE_MB = getattr(config, "MAX_FILE_SIZE_MB", 2048)

def register_media_handlers(app: Client):

    @app.on_message(filters.text & filters.private & ~filters.command(["start", "help", "about", "ping", "ban", "unban", "addsudo", "delsudo", "sudolist", "admins", "banlist", "banned", "stats", "broadcast", "setthumb", "viewthumb", "delthumb"]))
    async def text_link_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if is_banned(user_id):
            return await message.reply_text(
                Script.USER_BANNED_ALERT_TXT,
                parse_mode=enums.ParseMode.HTML
            )

        user_name = message.from_user.first_name or "User"

        # 1. Enforce Force-Sub
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

        # 2. Privacy & Copyright Safe Harbor: Auto-delete user link message after 10 minutes (600 seconds)
        asyncio.create_task(auto_delete_message(client, message.chat.id, message.id, delay_seconds=600))

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
                    cache_id = f"{user_id}_{int(time.time())}"
                    yt_payload = {
                        "title": yt_info["title"],
                        "author": yt_info["author"],
                        "thumbnail": yt_info.get("thumbnail"),
                        "download_links": yt_info["download_links"],
                        "best_audio_url": yt_info.get("best_audio_url"),
                        "video_id": yt_info.get("video_id"),
                        "original_url": url,
                        "user_id": user_id
                    }
                    yt_cache.set(cache_id, yt_payload)
                    yt_cache.set(str(user_id), yt_payload)

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
            status_msg = await message.reply_text(
                f"🔍 <i>Detecting & resolving {link_type.upper()} link via Sunil-SSBots API...</i>",
                reply_markup=get_cancel_button(user_id)
            )
            tmp_path = None
            meta = {}
            final_thumb_path = None
            task_start_time = time.time()

            try:
                queue_pos = await task_manager.acquire_slot(user_id, status_msg)
                if queue_pos > 0:
                    await status_msg.edit_text(
                        f"⚡ <b>ǫᴜᴇᴜᴇ sʟᴏᴛ ɢʀᴀɴᴛᴇᴅ!</b>\n<i>sᴛᴀʀᴛɪɴɢ ʏᴏᴜʀ {link_type.upper()} ᴅᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ...</i>",
                        parse_mode=enums.ParseMode.HTML,
                        reply_markup=get_cancel_button(user_id)
                    )

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

                if task_manager.is_cancelled(user_id):
                    raise TaskCancelledException()

                file_name = info["name"]
                file_size = info["size"]
                dlink = info["dlink"]

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
                task_manager.register_task_file(user_id, tmp_path)

                download_tracker = ProgressTracker(status_msg, f"⏬ Downloading: {file_name} ({file_size})", user_id=user_id)
                await download_file(dlink, tmp_path, download_tracker, user_id=user_id)

                if task_manager.is_cancelled(user_id):
                    raise TaskCancelledException()

                upload_tracker = ProgressTracker(status_msg, f"📤 Uploading via MTProto: {file_name}", user_id=user_id)

                async def upload_progress(current, total):
                    if task_manager.is_cancelled(user_id):
                        raise TaskCancelledException()
                    await upload_tracker.update(current, total)

                caption = Script.CAPTION_TXT.format(
                    file_name=file_name,
                    file_size=file_size,
                    provider=info["provider"],
                    deals_channel=DEALS_CHANNEL
                )

                ext = file_name.split(".")[-1].lower() if "." in file_name else ""
                if ext in ["mp4", "mkv", "webm", "mov", "avi"]:
                    await status_msg.edit_text(
                        f"⚡ <b>ᴇxᴛʀᴀᴄᴛɪɴɢ ᴠɪᴅᴇᴏ ᴅᴜʀᴀᴛɪᴏɴ & ᴛʜᴜᴍʙɴᴀɪʟ...</b>\n"
                        f"<blockquote>🎬 <i>ᴀɴᴀʟʏᴢɪɴɢ ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍ ʜᴇᴀᴅᴇʀs ᴠɪᴀ ғғᴍᴘᴇɢ...</i></blockquote>",
                        parse_mode=enums.ParseMode.HTML,
                        reply_markup=get_cancel_button(user_id)
                    )
                    meta = await get_video_metadata(tmp_path)
                    if meta.get("thumb"):
                        task_manager.register_task_file(user_id, meta["thumb"])

                    # Check for user custom thumbnail
                    final_thumb_path = await get_effective_thumbnail(client, user_id, meta.get("thumb"))
                    if final_thumb_path:
                        task_manager.register_task_file(user_id, final_thumb_path)

                    try:
                        await client.send_video(
                            chat_id=message.chat.id,
                            video=tmp_path,
                            caption=caption,
                            duration=meta.get("duration") or 0,
                            width=meta.get("width") or 1280,
                            height=meta.get("height") or 720,
                            thumb=final_thumb_path,
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

            except TaskCancelledException:
                print(f"[TASK CANCELLED] User {user_id} cancelled {link_type.upper()} task.")
                try:
                    await status_msg.edit_text(
                        "🚫 <b>ᴛᴀsᴋ ᴄᴀɴᴄᴇʟʟᴇᴅ!</b>\n\n<blockquote>🗑️ <i>All downloaded data & storage files have been wiped completely.</i></blockquote>",
                        parse_mode=enums.ParseMode.HTML
                    )
                except Exception:
                    pass
            except Exception as e:
                await status_msg.edit_text(
                    f"❌ <b>Error:</b> <code>{str(e)}</code>\n\n"
                    "Tip: Make sure the link is public and still accessible."
                )
            finally:
                # GUARANTEED SERVER HOSTING STORAGE CLEANUP
                task_manager.cleanup_user_files(user_id)
                await task_manager.release_slot(user_id)
