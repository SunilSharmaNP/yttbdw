import time
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import Message
import config
from translations import (
    Script,
    get_start_buttons,
    get_help_buttons,
    get_about_buttons,
    get_fsub_buttons,
)
from database.db import (
    OWNER_ID,
    sudo_users_set,
    banned_users_set,
    registered_users_set,
    bot_start_time,
    db,
    is_admin,
    is_banned,
    ban_user,
    unban_user,
    add_sudo_user,
    remove_sudo_user,
    db_add_user,
    set_user_thumbnail,
    get_user_thumbnail,
    del_user_thumbnail,
    get_all_broadcast_users,
)
from helpers.fsub import check_fsub, get_channel_invite
from helpers.logger import send_log
from core.queue import task_manager

UPDATES_CHANNEL = getattr(config, "UPDATES_CHANNEL", "SSBotsUpdates")
DEALS_CHANNEL = getattr(config, "DEALS_CHANNEL", "Tg_Shoping")
SUPPORT_CHAT = getattr(config, "SUPPORT_CHAT", "Sunil_Sharma_2_0_Bot")
OWNER_USERNAME = getattr(config, "OWNER_USERNAME", "Sunil_Sharma_2_0_Bot")
START_PIC = getattr(config, "START_PIC", "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1200&auto=format&fit=crop")
LOG_CHANNEL = getattr(config, "LOG_CHANNEL", None)
MAX_CONCURRENT_TASKS = getattr(config, "MAX_CONCURRENT_TASKS", 3)

def register_command_handlers(app: Client):

    @app.on_message(filters.command("start") & filters.private)
    async def start_handler(client: Client, message: Message):
        user = message.from_user
        user_id = user.id
        if is_banned(user_id):
            return await message.reply_text(Script.USER_BANNED_ALERT_TXT, parse_mode=enums.ParseMode.HTML)

        user_name = (user.first_name or "User").replace("<", "&lt;").replace(">", "&gt;")
        username = user.username or "None"

        is_new = db_add_user(user_id, user_name, username)
        if is_new:
            total_users = len(registered_users_set)
            if db is not None:
                try:
                    total_users = db.users.count_documents({})
                except Exception:
                    pass
            now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            await send_log(
                client,
                Script.LOG_NEW_USER_TXT.format(
                    user_id=user_id,
                    name=user_name,
                    username=username,
                    total_users=total_users,
                    timestamp=now_str
                )
            )

        is_joined, _, _ = await check_fsub(client, user_id)
        if not is_joined:
            updates_link = await get_channel_invite(client, UPDATES_CHANNEL)
            deals_link = await get_channel_invite(client, DEALS_CHANNEL)
            buttons = get_fsub_buttons(updates_link, deals_link, user_id)
            try:
                await message.reply_photo(
                    photo=START_PIC,
                    caption=Script.FORCE_SUB_TXT.format(user_name),
                    reply_markup=buttons,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception:
                await message.reply_text(
                    text=Script.FORCE_SUB_TXT.format(user_name),
                    reply_markup=buttons,
                    disable_web_page_preview=True,
                    parse_mode=enums.ParseMode.HTML
                )
            return

        bot_info = getattr(client, "me", None) or await client.get_me()
        bot_username = bot_info.username or "Bot"
        buttons = get_start_buttons(bot_username)

        try:
            await message.reply_photo(
                photo=START_PIC,
                caption=Script.START_TXT.format(user_name),
                reply_markup=buttons,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            await message.reply_text(
                text=Script.START_TXT.format(user_name),
                reply_markup=buttons,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )

    @app.on_message(filters.command("help") & filters.private)
    async def help_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if is_banned(user_id):
            return await message.reply_text(Script.USER_BANNED_ALERT_TXT, parse_mode=enums.ParseMode.HTML)

        user_name = message.from_user.first_name or "User"
        is_joined, _, _ = await check_fsub(client, user_id)
        if not is_joined:
            updates_link = await get_channel_invite(client, UPDATES_CHANNEL)
            deals_link = await get_channel_invite(client, DEALS_CHANNEL)
            buttons = get_fsub_buttons(updates_link, deals_link, user_id)
            try:
                return await message.reply_photo(
                    photo=START_PIC,
                    caption=Script.FORCE_SUB_TXT.format(user_name),
                    reply_markup=buttons,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception:
                return await message.reply_text(
                    text=Script.FORCE_SUB_TXT.format(user_name),
                    reply_markup=buttons,
                    disable_web_page_preview=True
                )

        try:
            await message.reply_photo(
                photo=START_PIC,
                caption=Script.HELP_TXT.format(SUPPORT_CHAT),
                reply_markup=get_help_buttons(),
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            await message.reply_text(
                text=Script.HELP_TXT.format(SUPPORT_CHAT),
                reply_markup=get_help_buttons(),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )

    @app.on_message(filters.command("about") & filters.private)
    async def about_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if is_banned(user_id):
            return await message.reply_text(Script.USER_BANNED_ALERT_TXT, parse_mode=enums.ParseMode.HTML)

        user_name = message.from_user.first_name or "User"
        is_joined, _, _ = await check_fsub(client, user_id)
        if not is_joined:
            updates_link = await get_channel_invite(client, UPDATES_CHANNEL)
            deals_link = await get_channel_invite(client, DEALS_CHANNEL)
            buttons = get_fsub_buttons(updates_link, deals_link, user_id)
            try:
                return await message.reply_photo(
                    photo=START_PIC,
                    caption=Script.FORCE_SUB_TXT.format(user_name),
                    reply_markup=buttons,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception:
                return await message.reply_text(
                    text=Script.FORCE_SUB_TXT.format(user_name),
                    reply_markup=buttons,
                    disable_web_page_preview=True
                )

        bot_info = getattr(client, "me", None) or await client.get_me()
        bot_username = bot_info.username or "Bot"
        bot_name = bot_info.first_name or "Media Downloader"
        try:
            await message.reply_photo(
                photo=START_PIC,
                caption=Script.ABOUT_TXT.format(bot_username, bot_name),
                reply_markup=get_about_buttons(),
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            await message.reply_text(
                text=Script.ABOUT_TXT.format(bot_username, bot_name),
                reply_markup=get_about_buttons(),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )

    @app.on_message(filters.command("ping") & filters.private)
    async def ping_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if is_banned(user_id):
            return await message.reply_text(Script.USER_BANNED_ALERT_TXT, parse_mode=enums.ParseMode.HTML)
        t1 = time.time()
        m = await message.reply_text("🏓 <i>Pinging server...</i>", parse_mode=enums.ParseMode.HTML)
        latency = round((time.time() - t1) * 1000, 2)
        await m.edit_text(f"🏓 <b>Pong!</b> <code>{latency} ms</code>\n✨ Bot is Online & Ready.")

    @app.on_message(filters.command("stats") & filters.private)
    async def stats_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            return await message.reply_text(Script.ADMIN_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        total_users = len(registered_users_set)
        total_downloads = 0
        if db is not None:
            try:
                total_users = db.users.count_documents({})
                total_downloads = db.downloads.count_documents({})
            except Exception:
                pass

        uptime_sec = int(time.time() - bot_start_time)
        hrs = uptime_sec // 3600
        mins = (uptime_sec % 3600) // 60
        secs = uptime_sec % 60
        uptime_str = f"{hrs}h {mins}m {secs}s"

        active_count = task_manager.active_count
        queue_count = len(task_manager.queue_waiters)
        banned_count = len(banned_users_set)
        sudo_count = len(sudo_users_set)

        db_type = "MongoDB (Persistent)" if db is not None else "In-Memory"
        log_channel_str = f"<code>{LOG_CHANNEL}</code>" if LOG_CHANNEL else "<i>Not Set</i>"

        text = (
            "📊 ── <b>ʙᴏᴛ sʏsᴛᴇᴍ sᴛᴀᴛɪsᴛɪᴄs</b> ── 📊\n\n"
            f"👥 <b>ᴛᴏᴛᴀʟ ᴜsᴇʀs :</b> <code>{total_users}</code>\n"
            f"📥 <b>ᴛᴏᴛᴀʟ ᴅᴏᴡɴʟᴏᴀᴅs :</b> <code>{total_downloads}</code>\n"
            f"⚡ <b>ᴀᴄᴛɪᴠᴇ ᴛᴀsᴋs :</b> <code>{active_count} / {MAX_CONCURRENT_TASKS}</code>\n"
            f"⏳ <b>ǫᴜᴇᴜᴇᴅ ᴛᴀsᴋs :</b> <code>{queue_count}</code>\n"
            f"🚫 <b>ʙᴀɴɴᴇᴅ ᴜsᴇʀs :</b> <code>{banned_count}</code>\n"
            f"🛡️ <b>sᴜᴅᴏ ᴀᴅᴍɪɴs :</b> <code>{sudo_count}</code>\n"
            f"📢 <b>ʟᴏɢ ᴄʜᴀɴɴᴇʟ :</b> {log_channel_str}\n"
            f"🗄️ <b>ᴅᴀᴛᴀʙᴀsᴇ :</b> <code>{db_type}</code>\n"
            f"⏱️ <b>ᴜᴘᴛɪᴍᴇ :</b> <code>{uptime_str}</code>"
        )
        await message.reply_text(text, parse_mode=enums.ParseMode.HTML)

    @app.on_message(filters.command("ban") & filters.private)
    async def ban_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            return await message.reply_text(Script.ADMIN_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        target_id = None
        target_name = "User"
        reason = "No reason provided"

        if message.reply_to_message and message.reply_to_message.from_user:
            target_id = message.reply_to_message.from_user.id
            target_name = message.reply_to_message.from_user.first_name or f"User {target_id}"
            if len(message.command) > 1:
                reason = " ".join(message.command[1:])
        elif len(message.command) > 1:
            try:
                target_id = int(message.command[1])
                target_name = f"User {target_id}"
                if len(message.command) > 2:
                    reason = " ".join(message.command[2:])
            except ValueError:
                return await message.reply_text(Script.BAN_USAGE_TXT, parse_mode=enums.ParseMode.HTML)
        else:
            return await message.reply_text(Script.BAN_USAGE_TXT, parse_mode=enums.ParseMode.HTML)

        if target_id == OWNER_ID or target_id in sudo_users_set:
            return await message.reply_text(Script.CANNOT_BAN_ADMIN, parse_mode=enums.ParseMode.HTML)

        if is_banned(target_id):
            return await message.reply_text(Script.ALREADY_BANNED.format(user_id=target_id), parse_mode=enums.ParseMode.HTML)

        ban_user(target_id, reason, user_id)
        admin_name = message.from_user.first_name or "Admin"

        await message.reply_text(
            Script.USER_BANNED_SUCCESS.format(user_id=target_id, reason=reason),
            parse_mode=enums.ParseMode.HTML
        )

        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        await send_log(
            client,
            Script.LOG_USER_BANNED_TXT.format(
                user_id=target_id,
                name=target_name,
                admin_id=user_id,
                admin_name=admin_name,
                reason=reason,
                timestamp=now_str
            )
        )

    @app.on_message(filters.command("unban") & filters.private)
    async def unban_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            return await message.reply_text(Script.ADMIN_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        target_id = None
        target_name = "User"

        if message.reply_to_message and message.reply_to_message.from_user:
            target_id = message.reply_to_message.from_user.id
            target_name = message.reply_to_message.from_user.first_name or f"User {target_id}"
        elif len(message.command) > 1:
            try:
                target_id = int(message.command[1])
                target_name = f"User {target_id}"
            except ValueError:
                return await message.reply_text(Script.UNBAN_USAGE_TXT, parse_mode=enums.ParseMode.HTML)
        else:
            return await message.reply_text(Script.UNBAN_USAGE_TXT, parse_mode=enums.ParseMode.HTML)

        if not is_banned(target_id):
            return await message.reply_text(Script.NOT_BANNED.format(user_id=target_id), parse_mode=enums.ParseMode.HTML)

        unban_user(target_id)
        admin_name = message.from_user.first_name or "Admin"

        await message.reply_text(
            Script.USER_UNBANNED_SUCCESS.format(user_id=target_id),
            parse_mode=enums.ParseMode.HTML
        )

        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        await send_log(
            client,
            Script.LOG_USER_UNBANNED_TXT.format(
                user_id=target_id,
                name=target_name,
                admin_id=user_id,
                admin_name=admin_name,
                timestamp=now_str
            )
        )

    @app.on_message(filters.command("addsudo") & filters.private)
    async def addsudo_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if user_id != OWNER_ID:
            return await message.reply_text(Script.OWNER_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        target_id = None
        if message.reply_to_message and message.reply_to_message.from_user:
            target_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                target_id = int(message.command[1])
            except ValueError:
                return await message.reply_text(Script.ADDSUDO_USAGE_TXT, parse_mode=enums.ParseMode.HTML)
        else:
            return await message.reply_text(Script.ADDSUDO_USAGE_TXT, parse_mode=enums.ParseMode.HTML)

        if target_id in sudo_users_set:
            return await message.reply_text(f"⚠️ <b>ᴜsᴇʀ <code>{target_id}</code> ɪs ᴀʟʀᴇᴀᴅʏ ᴀ sᴜᴅᴏ ᴀᴅᴍɪɴ!</b>", parse_mode=enums.ParseMode.HTML)

        add_sudo_user(target_id)
        await message.reply_text(f"✨ <b>ᴜsᴇʀ <code>{target_id}</code> ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ sᴜᴅᴏ ᴀᴅᴍɪɴs!</b>", parse_mode=enums.ParseMode.HTML)

    @app.on_message(filters.command("delsudo") & filters.private)
    async def delsudo_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if user_id != OWNER_ID:
            return await message.reply_text(Script.OWNER_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        target_id = None
        if message.reply_to_message and message.reply_to_message.from_user:
            target_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                target_id = int(message.command[1])
            except ValueError:
                return await message.reply_text(Script.DELSUDO_USAGE_TXT, parse_mode=enums.ParseMode.HTML)
        else:
            return await message.reply_text(Script.DELSUDO_USAGE_TXT, parse_mode=enums.ParseMode.HTML)

        if target_id == OWNER_ID:
            return await message.reply_text("⚠️ <b>ʏᴏᴜ ᴄᴀɴɴᴏᴛ ʀᴇᴍᴏᴠᴇ ᴛʜᴇ ʙᴏᴛ ᴏᴡɴᴇʀ ғʀᴏᴍ sᴜᴅᴏ!</b>", parse_mode=enums.ParseMode.HTML)

        if target_id not in sudo_users_set:
            return await message.reply_text(f"⚠️ <b>ᴜsᴇʀ <code>{target_id}</code> ɪs ɴᴏᴛ ᴀ sᴜᴅᴏ ᴀᴅᴍɪɴ!</b>", parse_mode=enums.ParseMode.HTML)

        remove_sudo_user(target_id)
        await message.reply_text(f"🗑️ <b>ᴜsᴇʀ <code>{target_id}</code> ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ sᴜᴅᴏ ᴀᴅᴍɪɴs!</b>", parse_mode=enums.ParseMode.HTML)

    @app.on_message(filters.command(["sudolist", "admins"]) & filters.private)
    async def sudolist_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            return await message.reply_text(Script.ADMIN_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        admins_text = f"👑 <b>ᴏᴡɴᴇʀ :</b> <code>{OWNER_ID}</code> (@{OWNER_USERNAME})\n\n🛡️ <b>sᴜᴅᴏ ᴀᴅᴍɪɴs ({len(sudo_users_set)}):</b>\n"
        for s_id in sorted(sudo_users_set):
            marker = " (Owner)" if s_id == OWNER_ID else ""
            admins_text += f"• <code>{s_id}</code>{marker}\n"

        await message.reply_text(admins_text, parse_mode=enums.ParseMode.HTML)

    @app.on_message(filters.command(["banlist", "banned"]) & filters.private)
    async def banlist_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            return await message.reply_text(Script.ADMIN_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        if not banned_users_set:
            return await message.reply_text("🟢 <b>ɴᴏ ᴜsᴇʀs ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ ʙᴀɴɴᴇᴅ!</b>", parse_mode=enums.ParseMode.HTML)

        text = f"🚫 <b>ʙᴀɴɴᴇᴅ ᴜsᴇʀs ({len(banned_users_set)}):</b>\n\n"
        for b_id in sorted(banned_users_set):
            text += f"• <code>{b_id}</code>\n"

        await message.reply_text(text, parse_mode=enums.ParseMode.HTML)

    # --- Command: /setthumb (Save Custom Video Thumbnail) ---
    @app.on_message(filters.command("setthumb") & filters.private)
    async def setthumb_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if is_banned(user_id):
            return await message.reply_text(Script.USER_BANNED_ALERT_TXT, parse_mode=enums.ParseMode.HTML)

        photo = None
        if message.photo:
            photo = message.photo
        elif message.reply_to_message and message.reply_to_message.photo:
            photo = message.reply_to_message.photo

        if not photo:
            return await message.reply_text(
                "📸 <b>ʜᴏᴡ ᴛᴏ sᴇᴛ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ :</b>\n\n"
                "• Send any photo to the bot directly, OR\n"
                "• Reply to a photo with <code>/setthumb</code>\n\n"
                "<i>All your future downloaded videos will automatically use this thumbnail!</i>",
                parse_mode=enums.ParseMode.HTML
            )

        set_user_thumbnail(user_id, photo.file_id)
        await message.reply_text(
            "✅ <b>ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ sᴀᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ! 🖼️</b>\n\n"
            "• Use <code>/viewthumb</code> to view your saved thumbnail.\n"
            "• Use <code>/delthumb</code> to delete and revert to automatic frame generator.",
            parse_mode=enums.ParseMode.HTML
        )

    # --- Command: /viewthumb (View Current Custom Thumbnail) ---
    @app.on_message(filters.command("viewthumb") & filters.private)
    async def viewthumb_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if is_banned(user_id):
            return await message.reply_text(Script.USER_BANNED_ALERT_TXT, parse_mode=enums.ParseMode.HTML)

        thumb_file_id = get_user_thumbnail(user_id)
        if not thumb_file_id:
            return await message.reply_text(
                "⚠️ <b>ɴᴏ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ sᴇᴛ!</b>\n\nSend a photo or reply with <code>/setthumb</code> to set one.",
                parse_mode=enums.ParseMode.HTML
            )

        await message.reply_photo(
            photo=thumb_file_id,
            caption="🖼️ <b>ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴄᴜsᴛᴏᴍ ᴠɪᴅᴇᴏ ᴛʜᴜᴍʙɴᴀɪʟ</b>\n\nSend <code>/delthumb</code> to remove it.",
            parse_mode=enums.ParseMode.HTML
        )

    # --- Command: /delthumb (Delete Custom Thumbnail) ---
    @app.on_message(filters.command("delthumb") & filters.private)
    async def delthumb_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if is_banned(user_id):
            return await message.reply_text(Script.USER_BANNED_ALERT_TXT, parse_mode=enums.ParseMode.HTML)

        existed = del_user_thumbnail(user_id)
        if existed:
            await message.reply_text(
                "🗑️ <b>ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ᴅᴇʟᴇᴛᴇᴅ!</b>\n\nVideos will now use automatic frame snapshots from FFmpeg.",
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await message.reply_text("⚠️ <b>ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ sᴀᴠᴇᴅ ᴛʜᴜᴍʙɴᴀɪʟ ᴛᴏ ᴅᴇʟᴇᴛᴇ.</b>", parse_mode=enums.ParseMode.HTML)

    # --- Automatic Photo Listener (Save as Thumbnail Prompt) ---
    @app.on_message(filters.photo & filters.private)
    async def photo_listener(client: Client, message: Message):
        user_id = message.from_user.id
        if is_banned(user_id):
            return
        set_user_thumbnail(user_id, message.photo.file_id)
        await message.reply_text(
            "🖼️ <b>ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ sᴀᴠᴇᴅ!</b>\n\nThis image will be attached to all your uploaded videos.\n• <code>/viewthumb</code> to view\n• <code>/delthumb</code> to remove",
            parse_mode=enums.ParseMode.HTML
        )

    # --- Command: /broadcast (Owner & Sudo Admins) ---
    @app.on_message(filters.command("broadcast") & filters.private)
    async def broadcast_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            return await message.reply_text(Script.ADMIN_ONLY_TXT, parse_mode=enums.ParseMode.HTML)

        broadcast_msg = message.reply_to_message
        broadcast_text = " ".join(message.command[1:]) if len(message.command) > 1 else None

        if not broadcast_msg and not broadcast_text:
            return await message.reply_text(
                "📢 <b>ʙʀᴏᴀᴅᴄᴀsᴛ ᴜsᴀɢᴇ :</b>\n\n"
                "• Reply to any message/photo/media with <code>/broadcast</code>, OR\n"
                "• Type: <code>/broadcast Your announcement message here...</code>",
                parse_mode=enums.ParseMode.HTML
            )

        all_target_users = get_all_broadcast_users()
        total_targets = len(all_target_users)

        if total_targets == 0:
            return await message.reply_text("⚠️ <b>No registered users found to broadcast.</b>", parse_mode=enums.ParseMode.HTML)

        status_msg = await message.reply_text(
            f"🚀 <b>Starting Broadcast to {total_targets} users...</b>\n\n⏳ <i>Please wait...</i>",
            parse_mode=enums.ParseMode.HTML
        )

        sent_count = 0
        failed_count = 0
        blocked_count = 0
        start_bc = time.time()

        for idx, target_uid in enumerate(all_target_users, start=1):
            try:
                if broadcast_msg:
                    await broadcast_msg.copy(chat_id=target_uid)
                else:
                    await client.send_message(
                        chat_id=target_uid,
                        text=f"📢 <b>[ᴀɴɴᴏᴜɴᴄᴇᴍᴇɴᴛ]</b>\n\n{broadcast_text}",
                        disable_web_page_preview=True,
                        parse_mode=enums.ParseMode.HTML
                    )
                sent_count += 1
            except Exception as e:
                err_str = str(e).lower()
                if "blocked" in err_str or "user is deactivated" in err_str:
                    blocked_count += 1
                else:
                    failed_count += 1

            if idx % 25 == 0 or idx == total_targets:
                try:
                    await status_msg.edit_text(
                        f"📢 <b>── ʙʀᴏᴀᴅᴄᴀsᴛ ɪɴ ᴘʀᴏɢʀᴇss ──</b>\n\n"
                        f"👥 <b>Total Targets:</b> <code>{total_targets}</code>\n"
                        f"✅ <b>Successfully Sent:</b> <code>{sent_count}</code>\n"
                        f"🚫 <b>Blocked/Dead:</b> <code>{blocked_count}</code>\n"
                        f"❌ <b>Errors:</b> <code>{failed_count}</code>\n"
                        f"⚡ <b>Progress:</b> <code>{idx}/{total_targets} ({(idx/total_targets)*100:.1f}%)</code>",
                        parse_mode=enums.ParseMode.HTML
                    )
                except Exception:
                    pass

        elapsed_sec = int(time.time() - start_bc)
        dur_str = f"{elapsed_sec}s" if elapsed_sec < 60 else f"{elapsed_sec//60}m {elapsed_sec%60}s"

        await status_msg.edit_text(
            f"✅ <b>── ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ──</b>\n\n"
            f"👥 <b>Total Targeted :</b> <code>{total_targets}</code>\n"
            f"✅ <b>Successfully Sent :</b> <code>{sent_count}</code>\n"
            f"🚫 <b>Blocked / Left :</b> <code>{blocked_count}</code>\n"
            f"❌ <b>Failed Deliveries :</b> <code>{failed_count}</code>\n"
            f"⏱️ <b>Time Taken :</b> <code>{dur_str}</code>",
            parse_mode=enums.ParseMode.HTML
        )

