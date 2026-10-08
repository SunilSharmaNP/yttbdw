# ==============================================================================
# 🤖 Bot Developer / Owner : Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ
# 🌐 Developer URL        : https://t.me/Sunil_Sharma_2_0_Bot (@Sunil_Sharma_2_0_Bot)
# 📢 Telegram Channel     : https://t.me/SSBotsUpdates (@SSBotsUpdates)
# 📺 YouTube Channel      : https://www.youtube.com/@SunilWebTricks (SunilWebTricks)
# 💬 Ask Doubt / Contact   : @Sunil_Sharma_2_0_Bot
# ==============================================================================

"""
Main Executable Entry Point for TeraBox & Diskwala Downloader Bot.
Dual Channel Force-Subscription Verification (Updates + Deals Channel)
High-Speed Chunked Download & 2GB Telegram MTProto Upload
"""

import os
import sys
import time
import asyncio
from datetime import datetime
import aiohttp
import aiofiles

from pyrogram import Client, filters, enums
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import config
from translations import Script, get_start_buttons, get_help_buttons, get_about_buttons, get_fsub_buttons
from resolvers import extract_urls, detect_link_type, resolve_terabox, resolve_diskwala, format_size

# Initialize Pyrogram MTProto Client
if config.SESSION_STRING:
    app = Client(
        name="terabox_session",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=config.SESSION_STRING
    )
elif config.BOT_TOKEN:
    app = Client(
        name="terabox_bot",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=config.BOT_TOKEN
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
    updates_ok = await check_membership(client, config.UPDATES_CHANNEL, user_id)
    deals_ok = await check_membership(client, config.DEALS_CHANNEL, user_id)
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
    headers = {"User-Agent": "Mozilla/5.0"}
    timeout = aiohttp.ClientTimeout(total=3600)
    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status not in (200, 206):
                raise Exception(f"Download HTTP {resp.status}")
            total = int(resp.headers.get("content-length") or 0)
            received = 0
            async with aiofiles.open(output_path, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 1024):
                    await f.write(chunk)
                    received += len(chunk)
                    await progress_tracker.update(received, total)
    return output_path

if app:
    # --- Command: /start ---
    @app.on_message(filters.command("start") & filters.private)
    async def start_handler(client: Client, message: Message):
        user = message.from_user
        user_id = user.id
        user_name = (user.first_name or "User").replace("<", "&lt;").replace(">", "&gt;")

        # 1. Check Dual Force-Sub
        is_joined, _, _ = await check_fsub(client, user_id)
        if not is_joined:
            updates_link = await get_channel_invite(client, config.UPDATES_CHANNEL)
            deals_link = await get_channel_invite(client, config.DEALS_CHANNEL)
            buttons = get_fsub_buttons(updates_link, deals_link, user_id)
            await message.reply_text(
                text=Script.FORCE_SUB_TXT.format(user_name),
                reply_markup=buttons,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
            return

        # 2. Main Start Menu
        bot_info = getattr(client, "me", None) or await client.get_me()
        bot_username = bot_info.username or "Bot"
        buttons = get_start_buttons(bot_username)
        await message.reply_text(
            text=Script.START_TXT.format(user_name, config.UPDATES_CHANNEL),
            reply_markup=buttons,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML
        )

    # --- Command: /help ---
    @app.on_message(filters.command("help") & filters.private)
    async def help_handler(client: Client, message: Message):
        is_joined, _, _ = await check_fsub(client, message.from_user.id)
        if not is_joined:
            updates_link = await get_channel_invite(client, config.UPDATES_CHANNEL)
            deals_link = await get_channel_invite(client, config.DEALS_CHANNEL)
            buttons = get_fsub_buttons(updates_link, deals_link, message.from_user.id)
            return await message.reply_text(
                text=Script.FORCE_SUB_TXT.format(message.from_user.first_name),
                reply_markup=buttons,
                disable_web_page_preview=True
            )

        await message.reply_text(
            text=Script.HELP_TXT.format(config.SUPPORT_CHAT),
            reply_markup=get_help_buttons(),
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML
        )

    # --- Command: /about ---
    @app.on_message(filters.command("about") & filters.private)
    async def about_handler(client: Client, message: Message):
        is_joined, _, _ = await check_fsub(client, message.from_user.id)
        if not is_joined:
            updates_link = await get_channel_invite(client, config.UPDATES_CHANNEL)
            deals_link = await get_channel_invite(client, config.DEALS_CHANNEL)
            buttons = get_fsub_buttons(updates_link, deals_link, message.from_user.id)
            return await message.reply_text(
                text=Script.FORCE_SUB_TXT.format(message.from_user.first_name),
                reply_markup=buttons,
                disable_web_page_preview=True
            )

        bot_info = getattr(client, "me", None) or await client.get_me()
        bot_username = bot_info.username or "Bot"
        bot_name = bot_info.first_name or "TeraBox Downloader"
        await message.reply_text(
            text=Script.ABOUT_TXT.format(bot_username, bot_name),
            reply_markup=get_about_buttons(),
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML
        )

    # --- Command: /ping ---
    @app.on_message(filters.command("ping") & filters.private)
    async def ping_handler(client: Client, message: Message):
        await message.reply_text("🏓 <b>Pong!</b> Pyrogram MTProto Bot is Online & Active.")

    # --- Callback Queries: Navigation & Force-Sub Verification ---
    @app.on_callback_query()
    async def callback_dispatcher(client: Client, query: CallbackQuery):
        data = query.data
        user_id = query.from_user.id
        user_name = (query.from_user.first_name or "User").replace("<", "&lt;").replace(">", "&gt;")
        bot_info = getattr(client, "me", None) or await client.get_me()
        bot_username = bot_info.username or "Bot"
        bot_name = bot_info.first_name or "TeraBox Downloader"

        # Verification Callback
        if data.startswith("verify_"):
            try:
                target_uid = int(data.split("_")[1])
                if user_id != target_uid:
                    return await query.answer("⚠️ 𝐓ʜɪs 𝐁ᴜᴛᴛᴏɴ 𝐈s 𝐍ᴏᴛ 𝐅ᴏʀ 𝐘ᴏᴜ!", show_alert=True)
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
                await query.message.edit_text(
                    text=Script.START_TXT.format(user_name, config.UPDATES_CHANNEL),
                    reply_markup=get_start_buttons(bot_username),
                    disable_web_page_preview=True,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception:
                pass
            return

        # Menu Navigation
        if data == "home":
            try:
                await query.message.edit_text(
                    text=Script.START_TXT.format(user_name, config.UPDATES_CHANNEL),
                    reply_markup=get_start_buttons(bot_username),
                    disable_web_page_preview=True,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception:
                pass

        elif data == "help":
            try:
                await query.message.edit_text(
                    text=Script.HELP_TXT.format(config.SUPPORT_CHAT),
                    reply_markup=get_help_buttons(),
                    disable_web_page_preview=True,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception:
                pass

        elif data == "about":
            try:
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

    # --- Message Handler: Auto Link Detection & 2GB MTProto Upload ---
    @app.on_message(filters.text & filters.private & ~filters.command(["start", "help", "about", "ping"]))
    async def text_link_handler(client: Client, message: Message):
        user_id = message.from_user.id
        user_name = message.from_user.first_name or "User"

        # 1. Enforce Force-Sub on link processing
        is_joined, _, _ = await check_fsub(client, user_id)
        if not is_joined:
            updates_link = await get_channel_invite(client, config.UPDATES_CHANNEL)
            deals_link = await get_channel_invite(client, config.DEALS_CHANNEL)
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

            status_msg = await message.reply_text(f"🔍 <i>Detecting & resolving {link_type.upper()} link...</i>")
            tmp_path = None

            try:
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
                if size_mb > config.MAX_FILE_SIZE_MB:
                    await status_msg.edit_text(
                        f"⚠️ <b>File exceeds limit:</b> {file_name} ({file_size})\n"
                        f"Maximum upload limit is {config.MAX_FILE_SIZE_MB} MB.\n\n"
                        f"🔗 <b>Direct Link:</b> <a href='{dlink}'>Click to Download</a>"
                    )
                    continue

                safe_name = "".join(c for c in file_name if c.isalnum() or c in "._- ").strip() or "file.mp4"
                tmp_path = os.path.join(config.DOWNLOAD_DIR, f"{int(time.time())}_{safe_name}")

                download_tracker = ProgressTracker(status_msg, f"⏬ Downloading: {file_name} ({file_size})")
                await download_file(dlink, tmp_path, download_tracker)

                upload_tracker = ProgressTracker(status_msg, f"📤 Uploading via MTProto: {file_name}")

                async def upload_progress(current, total):
                    await upload_tracker.update(current, total)

                caption = Script.CAPTION_TXT.format(
                    file_name=file_name,
                    file_size=file_size,
                    provider=info["provider"],
                    deals_channel=config.DEALS_CHANNEL
                )

                ext = file_name.split(".")[-1].lower() if "." in file_name else ""
                if ext in ["mp4", "mkv", "webm", "mov"]:
                    try:
                        await client.send_video(
                            chat_id=message.chat.id,
                            video=tmp_path,
                            caption=caption,
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

                await status_msg.delete()

            except Exception as e:
                await status_msg.edit_text(
                    f"❌ <b>Error:</b> <code>{str(e)}</code>\n\n"
                    "Tip: Make sure the link is public and still accessible."
                )
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except Exception:
                        pass

async def send_deploy_log(client: Client):
    """Sends deployment status notification to log channel if configured."""
    if not config.LOG_CHANNEL:
        return
    try:
        log_text = (
            "🚀 <b>TeraBox & Diskwala Bot Deployed!</b>\n\n"
            f"👤 <b>Developer:</b> <a href='{config.DEVELOPER_URL}'>{config.DEVELOPER_NAME}</a>\n"
            f"📢 <b>Updates:</b> <a href='{config.CHANNEL_URL}'>@SSBotsUpdates</a>\n"
            f"📺 <b>YouTube:</b> <a href='{config.YOUTUBE_URL}'>SunilWebTricks</a>\n"
            f"🛍️ <b>Deals:</b> @{config.DEALS_CHANNEL}\n"
            f"🕒 <b>Deployed At:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            "⚡ <b>Engine:</b> Pyrogram MTProto (2GB File Upload Ready)"
        )
        await client.send_message(
            chat_id=config.LOG_CHANNEL,
            text=log_text,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        print(f"[DEPLOY LOG WARNING] Could not send to log channel: {e}")

def run():
    if not app:
        print("[ERROR] Please configure API_ID, API_HASH, and BOT_TOKEN in .env file!")
        sys.exit(1)

    deploy_banner = (
        "====================================================================\n"
        f"🚀 TERA BOX & DISKWALA PYROGRAM BOT DEPLOYED SUCCESSFULLY!\n"
        f"👤 Developer / Owner: {config.DEVELOPER_NAME} ({config.DEVELOPER_URL})\n"
        f"📢 Telegram Channel : {config.CHANNEL_URL} (@{config.UPDATES_CHANNEL})\n"
        f"📺 YouTube Channel  : {config.YOUTUBE_URL} (SunilWebTricks)\n"
        f"💬 Ask Doubt/Support: @{config.SUPPORT_CHAT}\n"
        "===================================================================="
    )
    print(deploy_banner)

    async def main_startup():
        async with app:
            me = await app.get_me()
            print(f"🤖 Bot Online as @{me.username} ({me.first_name})")
            await send_deploy_log(app)
            print("⚡ Bot is listening for updates...")
            # Keep running
            while True:
                await asyncio.sleep(3600)

    try:
        app.run()
    except Exception as e:
        print(f"Bot execution error: {e}")

if __name__ == "__main__":
    run()
