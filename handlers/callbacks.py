import os
import time
from datetime import datetime
from pyrogram import Client, enums
from pyrogram.types import CallbackQuery
import config
from translations import (
    Script,
    get_start_buttons,
    get_help_buttons,
    get_about_buttons,
)
from database.db import (
    is_banned,
    db_log_download,
)
from helpers.fsub import check_fsub
from helpers.logger import send_log
from helpers.cache import yt_cache
from helpers.progress import ProgressTracker, download_file, get_cancel_button
from helpers.ffmpeg import mux_media_ffmpeg, convert_to_mp3_ffmpeg, get_video_metadata
from helpers.privacy import get_effective_thumbnail
from helpers.youtube_download import download_youtube_stream
from core.queue import task_manager, TaskCancelledException
from resolvers import format_size

DEALS_CHANNEL = getattr(config, "DEALS_CHANNEL", "Tg_Shoping")
SUPPORT_CHAT = getattr(config, "SUPPORT_CHAT", "Sunil_Sharma_2_0_Bot")
DOWNLOAD_DIR = getattr(config, "DOWNLOAD_DIR", "./downloads")
START_PIC = getattr(config, "START_PIC", "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1200&auto=format&fit=crop")

def register_callback_handlers(app: Client):

    @app.on_callback_query()
    async def callback_dispatcher(client: Client, query: CallbackQuery):
        data = query.data
        user_id = query.from_user.id
        print(f"[CALLBACK] Received click: {data} from user {user_id}")

        if is_banned(user_id):
            return await query.answer("⛔ You are banned from using this bot!", show_alert=True)

        user_name = (query.from_user.first_name or "User").replace("<", "&lt;").replace(">", "&gt;")
        bot_info = getattr(client, "me", None) or await client.get_me()
        bot_username = bot_info.username or "Bot"
        bot_name = bot_info.first_name or "Media Downloader"

        # 0. Task Cancellation Callback (Cancel button pressed during download/upload)
        if data.startswith("cancel_"):
            try:
                target_uid = int(data.split("_")[1])
                if user_id != target_uid:
                    return await query.answer("⚠️ You can only cancel your own task!", show_alert=True)

                task_manager.cancel_user_task(user_id)
                await query.answer("🛑 Task Cancelled! Storage wiped.", show_alert=True)
                await query.message.edit_text(
                    "🚫 <b>ᴛᴀsᴋ ᴄᴀɴᴄᴇʟʟᴇᴅ ʙʏ ᴜsᴇʀ!</b>\n\n"
                    "<blockquote>🗑️ <i>All active download streams have been aborted and storage files cleared completely from hosting server.</i></blockquote>",
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception as e:
                await query.answer(f"Cancel notice: {e}", show_alert=False)
            return

        # 1. Force-Sub Verification Callback
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

        # 2. YouTube Quality Download Callback (ytq:{cache_id}:{idx} or ytq_{cache_id}_{idx})
        if data.startswith("ytq:") or data.startswith("ytq_"):
            try:
                if data.startswith("ytq:"):
                    parts = data.split(":")
                    cache_id = parts[1]
                    idx = int(parts[2])
                else:
                    parts = data.split("_")
                    idx = int(parts[-1])
                    cache_id = "_".join(parts[1:-1])
            except Exception as e:
                print(f"[CALLBACK ERROR] Failed to parse YouTube callback data '{data}': {e}")
                return await query.answer("⚠️ Invalid quality parameter.", show_alert=True)

            cached = yt_cache.get(cache_id) or yt_cache.get(str(user_id))
            if not cached:
                print(f"[CALLBACK ERROR] YouTube cache miss for cache_id={cache_id}, user={user_id}")
                return await query.answer("⚠️ Session Expired! Please re-send the YouTube link.", show_alert=True)

            download_links = cached.get("download_links", [])
            if idx >= len(download_links):
                return await query.answer("⚠️ Invalid Quality selection.", show_alert=True)

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
            final_thumb_path = None

            try:
                queue_pos = await task_manager.acquire_slot(user_id, status_msg)
                if queue_pos > 0:
                    await status_msg.edit_text(
                        f"⚡ <b>ǫᴜᴇᴜᴇ sʟᴏᴛ ɢʀᴀɴᴛᴇᴅ!</b>\n<i>sᴛᴀʀᴛɪɴɢ ʏᴏᴜʀ {fmt} ᴅᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ...</i>",
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
                        provider=f"YouTube ({fmt.upper()})",
                        link_or_title=title,
                        queue_status=queue_status_text,
                        timestamp=now_str
                    )
                )

                target_yt_url = cached.get("original_url") or (
                    f"https://www.youtube.com/watch?v={cached.get('video_id')}"
                    if cached.get("video_id")
                    else None
                )

                if itype == "audio":
                    target_audio_url = video_url or audio_url
                    if not target_audio_url and not target_yt_url:
                        raise Exception("Audio stream URL not found.")

                    raw_audio_path = os.path.join(DOWNLOAD_DIR, f"{ts}_a_{safe_title}.m4a")
                    task_manager.register_task_file(user_id, raw_audio_path)

                    await status_msg.edit_text(
                        f"🎵 <b>Downloading Audio Stream:</b> <code>{title}</code>\n"
                        f"📦 <b>Format:</b> <code>{fmt.upper()}</code>\n"
                        f"<blockquote>⚡ <i>Connecting to high-speed audio stream...</i></blockquote>",
                        reply_markup=get_cancel_button(user_id)
                    )
                    audio_tracker = ProgressTracker(status_msg, f"🎵 Downloading Audio: {title}", user_id=user_id)
                    downloaded_audio_path, _ = await download_youtube_stream(
                        stream_url=target_audio_url,
                        output_path=raw_audio_path,
                        progress_tracker=audio_tracker,
                        user_id=user_id,
                        original_url=target_yt_url,
                        quality_tag="audio",
                        is_audio=True,
                        status_msg=status_msg
                    )

                    upload_file_path = downloaded_audio_path
                    file_name = f"{safe_title}_{fmt}.m4a"

                    if fmt.lower() == "mp3":
                        mp3_path = os.path.join(DOWNLOAD_DIR, f"{ts}_{safe_title}.mp3")
                        task_manager.register_task_file(user_id, mp3_path)
                        await status_msg.edit_text(
                            f"⚡ <b>Converting Audio to MP3 (192kbps)...</b>\n"
                            f"<blockquote>🎬 <i>Encoding with FFmpeg...</i></blockquote>",
                            reply_markup=get_cancel_button(user_id)
                        )
                        if await convert_to_mp3_ffmpeg(upload_file_path, mp3_path):
                            upload_file_path = mp3_path
                            file_name = f"{safe_title}.mp3"

                    if task_manager.is_cancelled(user_id):
                        raise TaskCancelledException()

                    file_size_bytes = os.path.getsize(upload_file_path)
                    file_size_human = format_size(file_size_bytes)
                    upload_tracker = ProgressTracker(status_msg, f"📤 Uploading Audio to Telegram: {title}", user_id=user_id)
                    async def upload_progress(current, total):
                        if task_manager.is_cancelled(user_id):
                            raise TaskCancelledException()
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
                    v_ext = selected.get("ext") or "mp4"
                    raw_video_path = os.path.join(DOWNLOAD_DIR, f"{ts}_v_{safe_title}.{v_ext}")
                    muxed_path = os.path.join(DOWNLOAD_DIR, f"{ts}_{safe_title}_{fmt}.mp4")
                    task_manager.register_task_file(user_id, raw_video_path)

                    await status_msg.edit_text(
                        f"⏬ <b>Downloading via Aria2c (16 Conns):</b> <code>{title}</code>\n"
                        f"📦 <b>Quality:</b> <code>{fmt}</code>\n"
                        f"<blockquote>⚡ <i>Multi-threaded high-speed DDL stream...</i></blockquote>",
                        reply_markup=get_cancel_button(user_id)
                    )
                    video_tracker = ProgressTracker(status_msg, f"⏬ Aria2c Downloading: {fmt}", user_id=user_id)
                    final_upload_path = raw_video_path
                    file_name = f"{safe_title}_{fmt}.{v_ext}"

                    downloaded_path, was_fallback = await download_youtube_stream(
                        stream_url=video_url,
                        output_path=raw_video_path,
                        progress_tracker=video_tracker,
                        user_id=user_id,
                        original_url=target_yt_url,
                        quality_tag=fmt,
                        is_audio=False,
                        status_msg=status_msg
                    )

                    final_upload_path = downloaded_path
                    # Check if separate audio muxing is explicitly needed (only if audio_url provided and different from video_url)
                    if audio_url and audio_url != video_url and selected.get("needs_muxing"):
                        task_manager.register_task_file(user_id, muxed_path)
                        raw_audio_path = os.path.join(DOWNLOAD_DIR, f"{ts}_a_{safe_title}.m4a")
                        task_manager.register_task_file(user_id, raw_audio_path)
                        await status_msg.edit_text(
                            f"🎵 <b>Downloading High-Quality Audio Track...</b>\n"
                            f"<blockquote>⚡ <i>Fetching audio stream via aria2c...</i></blockquote>",
                            reply_markup=get_cancel_button(user_id)
                        )
                        audio_tracker = ProgressTracker(status_msg, "🎵 Audio Track", user_id=user_id)
                        downloaded_audio, _ = await download_youtube_stream(
                            stream_url=audio_url,
                            output_path=raw_audio_path,
                            progress_tracker=audio_tracker,
                            user_id=user_id,
                            original_url=target_yt_url,
                            quality_tag="audio",
                            is_audio=True,
                            status_msg=status_msg
                        )

                        if task_manager.is_cancelled(user_id):
                            raise TaskCancelledException()

                        await status_msg.edit_text(
                            f"⚡ <b>Fast Muxing Video + Audio via FFmpeg...</b>\n"
                            f"<blockquote>🎬 <i>Synchronizing media into single MP4 file...</i></blockquote>",
                            reply_markup=get_cancel_button(user_id)
                        )
                        is_muxed = await mux_media_ffmpeg(raw_video_path, downloaded_audio, muxed_path)
                        if is_muxed:
                            final_upload_path = muxed_path
                            file_name = f"{safe_title}_{fmt}.mp4"

                    if task_manager.is_cancelled(user_id):
                        raise TaskCancelledException()

                    meta = await get_video_metadata(final_upload_path)
                    file_size_bytes = os.path.getsize(final_upload_path)
                    file_size_human = format_size(file_size_bytes)

                    await status_msg.edit_text(
                        f"📤 <b>Uploading Video to Telegram:</b> <code>{file_name}</code>\n"
                        f"💾 <b>Size:</b> <code>{file_size_human}</code>\n"
                        f"<blockquote>⚡ <i>Streaming via 2GB MTProto engine...</i></blockquote>",
                        reply_markup=get_cancel_button(user_id)
                    )
                    upload_tracker = ProgressTracker(status_msg, f"📤 Uploading: {file_name}", user_id=user_id)
                    async def upload_progress(current, total):
                        if task_manager.is_cancelled(user_id):
                            raise TaskCancelledException()
                        await upload_tracker.update(current, total)

                    caption = Script.CAPTION_TXT.format(
                        file_name=file_name,
                        file_size=file_size_human,
                        provider=f"YouTube ({fmt})",
                        deals_channel=DEALS_CHANNEL
                    )

                    if meta.get("thumb"):
                        task_manager.register_task_file(user_id, meta["thumb"])

                    final_thumb_path = await get_effective_thumbnail(client, user_id, meta.get("thumb"))
                    if final_thumb_path:
                        task_manager.register_task_file(user_id, final_thumb_path)

                    try:
                        await client.send_video(
                            chat_id=query.message.chat.id,
                            video=final_upload_path,
                            caption=caption,
                            duration=meta.get("duration") or 0,
                            width=meta.get("width") or 1280,
                            height=meta.get("height") or 720,
                            thumb=final_thumb_path,
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

            except TaskCancelledException:
                print(f"[TASK CANCELLED] User {user_id} cancelled YouTube {fmt} task.")
                try:
                    await status_msg.edit_text(
                        "🚫 <b>ᴛᴀsᴋ ᴄᴀɴᴄᴇʟʟᴇᴅ!</b>\n\n<blockquote>🗑️ <i>All downloaded data & storage files have been wiped completely.</i></blockquote>",
                        parse_mode=enums.ParseMode.HTML
                    )
                except Exception:
                    pass
            except Exception as e:
                print(f"[YOUTUBE DOWNLOAD ERROR] User {user_id}: {e}")
                try:
                    await status_msg.edit_text(
                        f"❌ <b>Download Error:</b> <code>{str(e)}</code>\n\n"
                        f"🔗 <b>Direct Video Link:</b> <a href='{video_url}'>Click here</a>"
                    )
                except Exception:
                    pass
            finally:
                # COMPLETE STORAGE CLEAR ON HOSTING SERVER
                task_manager.cleanup_user_files(user_id)
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
