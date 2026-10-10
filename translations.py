# ==============================================================================
# 🤖 Bot Developer / Owner : Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ
# 🌐 Developer URL        : https://t.me/Sunil_Sharma_2_0_Bot (@Sunil_Sharma_2_0_Bot)
# 📢 Telegram Channel     : https://t.me/SSBotsUpdates (@SSBotsUpdates)
# 📺 YouTube Channel      : https://www.youtube.com/@SunilWebTricks (SunilWebTricks)
# 💬 Support Chat         : @Sunil_Sharma_2_0_Bot
# ==============================================================================

try:
    from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
except ImportError:
    class InlineKeyboardButton:
        def __init__(self, text="", callback_data=None, url=None):
            self.text = text
            self.callback_data = callback_data
            self.url = url
    class InlineKeyboardMarkup:
        def __init__(self, inline_keyboard=None):
            self.inline_keyboard = inline_keyboard or []
import config

# Safe fallbacks in case config attributes are missing
DEALS_CHANNEL = getattr(config, "DEALS_CHANNEL", "Tg_Shoping")
UPDATES_CHANNEL = getattr(config, "UPDATES_CHANNEL", "SSBotsUpdates")
DEVELOPER_NAME = getattr(config, "DEVELOPER_NAME", "Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ")
DEVELOPER_URL = getattr(config, "DEVELOPER_URL", "https://t.me/Sunil_Sharma_2_0_Bot")
CHANNEL_URL = getattr(config, "CHANNEL_URL", "https://t.me/SSBotsUpdates")
YOUTUBE_URL = getattr(config, "YOUTUBE_URL", "https://www.youtube.com/@SunilWebTricks")
SUPPORT_CHAT = getattr(config, "SUPPORT_CHAT", "Sunil_Sharma_2_0_Bot")
OWNER_USERNAME = getattr(config, "OWNER_USERNAME", "Sunil_Sharma_2_0_Bot")
START_PIC = getattr(config, "START_PIC", "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1200&auto=format&fit=crop")

class Script:
    START_PIC = START_PIC
    START_TXT = """<blockquote><b>👋 ʜᴇʟʟᴏ {} ! 🌺</b></blockquote>

🤖 <b>ɪ ᴀᴍ ᴛʜᴇ ғᴀsᴛᴇsᴛ ᴛᴇʀᴀʙᴏx, ᴅɪsᴋᴡᴀʟᴀ & ʏᴏᴜᴛᴜʙᴇ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ⚡</b>

📁 <b>sᴇɴᴅ ᴍᴇ ᴀɴʏ sᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋ, ɪ ᴡɪʟʟ :</b>
• 🔍 <b>ɪɴsᴛᴀɴᴛʟʏ ᴅᴇᴛᴇᴄᴛ & ᴇxᴛʀᴀᴄᴛ ᴛʜᴇ ғɪʟᴇ</b>
• ⏬ <b>ᴅᴏᴡɴʟᴏᴀᴅ ᴀᴛ ᴜʟᴛʀᴀ ʜɪɢʜ sᴘᴇᴇᴅ</b>
• 📤 <b>ᴜᴘʟᴏᴀᴅ ᴅɪʀᴇᴄᴛʟʏ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ (ᴜᴘ ᴛᴏ 2ɢʙ) 🚀</b>

━༻« ★ <b>sᴘᴇᴄɪᴀʟ ғᴇᴀᴛᴜʀᴇs</b> ★ »༺━
<blockquote>• <b>ᴜɴʟɪᴍɪᴛᴇᴅ 2ɢʙ ᴍᴛᴘʀᴏᴛᴏ ᴜᴘʟᴏᴀᴅs</b> 
• <b>sᴜᴘᴘᴏʀᴛs ᴀʟʟ 20+ ᴛᴇʀᴀʙᴏx ᴍɪʀʀᴏʀ ᴅᴏᴍᴀɪɴs</b>
• <b>ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ (360ᴘ, 720ᴘ, 1080ᴘ) & ᴍᴘ3 ᴀᴜᴅɪᴏ</b>
• <b>ᴅɪsᴋᴡᴀʟᴀ ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ</b>
• <b>ʟɪᴠᴇ ᴅᴏᴡɴʟᴏᴀᴅ & ᴜᴘʟᴏᴀᴅ ᴘʀᴏɢʀᴇss ʙᴀʀs</b></blockquote>

⭐ <b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ <a href='https://t.me/SSBotsUpdates'>★彡 🅂🅂🄱🄾🅃🅂 彡★</a></b>"""

    HELP_TXT = """<blockquote><b>📘 ── ʜᴇʟᴘ & ᴜsᴀɢᴇ ɢᴜɪᴅᴇ ── 📖</b></blockquote>

💫 <b>ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ & ʀᴇᴄᴇɪᴠᴇ ғɪʟᴇs :</b>

🚀 <b>sᴛᴇᴘ 1 : sᴇɴᴅ ʟɪɴᴋ</b>
<blockquote>• ᴄᴏᴘʏ ᴀɴʏ <b>ᴛᴇʀᴀʙᴏx</b> (terabox.com, 1024terabox.com, etc.), <b>ʏᴏᴜᴛᴜʙᴇ</b>, ᴏʀ <b>ᴅɪsᴋᴡᴀʟᴀ</b> ʟɪɴᴋ.
• ᴘᴀsᴛᴇ ɪᴛ ᴅɪʀᴇᴄᴛʟʏ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.</blockquote>

⚡ <b>sᴛᴇᴘ 2 : ǫᴜᴀʟɪᴛʏ sᴇʟᴇᴄᴛɪᴏɴ (ғᴏʀ ʏᴏᴜᴛᴜʙᴇ)</b>
<blockquote>• ғᴏʀ ʏᴏᴜᴛᴜʙᴇ, ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ᴇxᴛʀᴀᴄᴛ ᴀʟʟ ᴠɪᴅᴇᴏ (1080ᴘ, 720ᴘ, 480ᴘ, 360ᴘ) & ᴍᴘ3 ᴀᴜᴅɪᴏ ғᴏʀᴍᴀᴛs.
• ᴛᴀᴘ ʏᴏᴜʀ ᴅᴇsɪʀᴇᴅ ǫᴜᴀʟɪᴛʏ ʙᴜᴛᴛᴏɴ!</blockquote>

📤 <b>sᴛᴇᴘ 3 : ᴛᴇʟᴇɢʀᴀᴍ ᴜᴘʟᴏᴀᴅ</b>
<blockquote>• ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ ᴍᴇᴅɪᴀ ᴅɪʀᴇᴄᴛʟʏ ᴛᴏ ʏᴏᴜ (ᴜᴘ ᴛᴏ <b>2 ɢʙ</b>).
• ᴠɪᴅᴇᴏs ᴀʀᴇ ᴜᴘʟᴏᴀᴅᴇᴅ ᴡɪᴛʜ ғᴜʟʟ ᴅᴜʀᴀᴛɪᴏɴ & sᴛʀᴇᴀᴍɪɴɢ sᴜᴘᴘᴏʀᴛ!</blockquote>

<blockquote>⚠️ <b>ʀᴇᴘᴏʀᴛ ɪssᴜᴇ: <a href='https://t.me/Sunil_Sharma_2_0_Bot'>𓆩Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ [🇳🇵]𓆪</a></b></blockquote>"""

    ABOUT_TXT = """<blockquote><b>🌟 ── ᴀʙᴏᴜᴛ ᴍᴇ • ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ── 🌟</b></blockquote>

📌 <b>ɪ ᴀᴍ ʏᴏᴜʀ ᴜʟᴛɪᴍᴀᴛᴇ ᴛᴇʀᴀʙᴏx, ᴅɪsᴋᴡᴀʟᴀ & ʏᴏᴜᴛᴜʙᴇ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ⚡</b>

‣ <b>ᴍʏ ɴᴀᴍᴇ :</b> <a href="https://t.me/{}">{}</a>
‣ <b>ᴅᴇᴠᴇʟᴏᴘᴇʀ :</b> <a href="https://t.me/Sunil_Sharma_2_0_Bot">𓆩Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ [🇳🇵]𓆪</a>
‣ <b>ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ :</b> <a href="https://t.me/SSBotsUpdates">ss ʙᴏᴛs ᴜᴘᴅᴀᴛᴇs</a>
‣ <b>ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ :</b> <a href="https://www.youtube.com/@SunilWebTricks">SunilWebTricks</a>
‣ <b>ʟᴀɴɢᴜᴀɢᴇ :</b> <a href="https://www.python.org/">ᴘʏᴛʜᴏɴ 3.10+</a>
‣ <b>ғʀᴀᴍᴇᴡᴏʀᴋ :</b> <a href="https://docs.pyrogram.org/">ᴘʏʀᴏɢʀᴀᴍ &amp; ᴛɢᴄʀʏᴘᴛᴏ</a>
‣ <b>ᴜᴘʟᴏᴀᴅ ʟɪᴍɪᴛ :</b> <code>2,048 ᴍʙ (2 ɢʙ ᴍᴛᴘʀᴏᴛᴏ)</code>
‣ <b>ʙᴜɪʟᴅ sᴛᴀᴛᴜs :</b> <code>v3.5.0 [ sᴛᴀʙʟᴇ &amp; ᴏᴘᴛɪᴍɪᴢᴇᴅ ]</code>

<i>💖 ɪғ ʏᴏᴜ ғɪɴᴅ ᴍᴇ ᴜsᴇғᴜʟ, ᴘʟᴇᴀsᴇ ᴄᴏɴsɪᴅᴇʀ sʜᴀʀɪɴɢ ᴍᴇ ᴡɪᴛʜ ʏᴏᴜʀ ғʀɪᴇɴᴅs!</i>"""

    FORCE_SUB_TXT = """<blockquote><b>🔐 ── ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʀᴇǫᴜɪʀᴇᴅ ── 🔐</b></blockquote>

👋 <b>ʜᴇʟʟᴏ {} ! 🌺</b>

😇 <b>ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ʙᴏᴛʜ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ :</b>

📢 <b>1. ʙᴏᴛ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ</b>
🛍️ <b>2. ʟᴏᴏᴛ ᴅᴇᴀʟs ᴄʜᴀɴɴᴇʟ</b>

👉 <i>ᴄʟɪᴄᴋ ʙᴏᴛʜ ‘ᴊᴏɪɴ’ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ, ᴛʜᴇɴ ᴛᴀᴘ ‘✅ ᴠᴇʀɪғʏ’ ᴛᴏ ᴜɴʟᴏᴄᴋ!</i>"""

    YT_WAIT_TXT = """<blockquote><b>⏳ ── ᴇxᴛʀᴀᴄᴛɪɴɢ ʏᴏᴜᴛᴜʙᴇ ǫᴜᴀʟɪᴛɪᴇs ── 🎬</b></blockquote>

🔍 <b>ʟᴏᴀᴅɪɴɢ ᴀʟʟ ᴠɪᴅᴇᴏ & ᴀᴜᴅɪᴏ ғᴏʀᴍᴀᴛs...</b>

<blockquote>⚡ <i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ ғᴇᴡ sᴇᴄᴏɴᴅs. ᴏᴜʀ ʜɪɢʜ-sᴘᴇᴇᴅ ᴇɴɢɪɴᴇ ɪs ᴇxᴛʀᴀᴄᴛɪɴɢ ᴀʟʟ ᴠᴇʀɪғɪᴇᴅ ǫᴜᴀʟɪᴛɪᴇs (1080ᴘ, 720ᴘ, 480ᴘ, 360ᴘ &amp; ᴍᴘ3)...</i></blockquote>"""

    YT_INFO_TXT = """<blockquote><b>🎬 ── ʏᴏᴜᴛᴜʙᴇ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ── 🎬</b></blockquote>

📌 <b>ᴛɪᴛʟᴇ :</b> <code>{title}</code>
👤 <b>ᴄʜᴀɴɴᴇʟ :</b> <code>{author}</code>

👇 <b>sᴇʟᴇᴄᴛ ᴀ ǫᴜᴀʟɪᴛʏ ʙᴇʟᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ & ᴜᴘʟᴏᴀᴅ :</b>"""

    CAPTION_TXT = """<b>📂 ғɪʟᴇɴᴀᴍᴇ :</b> <code>{file_name}</code>
💾 <b>ғɪʟᴇ sɪᴢᴇ :</b> <code>{file_size}</code>
🌐 <b>sᴏᴜʀᴄᴇ :</b> <code>{provider}</code>

♻️ <b>ғᴏʀ ʟᴏᴏᴛ ᴅᴇᴀʟs ᴏғғᴇʀs 🔥</b>
📌 <b>ᴊᴏɪɴ :</b> @{deals_channel}

<blockquote>⚡ <b>ᴜᴘʟᴏᴀᴅᴇᴅ ʙʏ <a href='https://t.me/SSBotsUpdates'>★彡 🅂🅂🄱🄾🅃🅂 彡★</a> • 2ɢʙ ᴍᴛᴘʀᴏᴛᴏ</b></blockquote>"""

    TASK_ALREADY_RUNNING_TXT = """<blockquote>⚠️ ── <b>ᴛᴀsᴋ ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ</b> ── ⚠️</blockquote>

🚫 <b>ʜᴇʏ {} !</b>
ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ᴅᴏᴡɴʟᴏᴀᴅ ᴛᴀsᴋ ɪɴ ᴘʀᴏɢʀᴇss. ᴏɴʟʏ <b>1 ᴛᴀsᴋ</b> ɪs ᴀʟʟᴏᴡᴇᴅ ᴀᴛ ᴀ ᴛɪᴍᴇ.

<blockquote>⏳ <i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴛᴀsᴋ ᴛᴏ ᴄᴏᴍᴘʟᴇᴛᴇ ʙᴇғᴏʀᴇ sᴛᴀʀᴛɪɴɢ ᴀ ɴᴇᴡ ᴏɴᴇ!</i></blockquote>"""

    TASK_COOLDOWN_TXT = """<blockquote>⏳ ── <b>ᴄᴏᴏʟᴅᴏᴡɴ ᴀᴄᴛɪᴠᴇ</b> ── ⏳</blockquote>

⏰ <b>ʜᴇʏ {} !</b>
ʏᴏᴜʀ ᴘʀᴇᴠɪᴏᴜs ᴛᴀsᴋ ᴡᴀs ᴄᴏᴍᴘʟᴇᴛᴇᴅ ʀᴇᴄᴇɴᴛʟʏ.

<blockquote>🛑 <i>ᴛᴏ ᴘʀᴇᴠᴇɴᴛ sᴘᴀᴍ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ <b>{} sᴇᴄᴏɴᴅs</b> ʙᴇғᴏʀᴇ sᴛᴀʀᴛɪɴɢ ᴀ ɴᴇᴡ ᴛᴀsᴋ! (1 ᴍɪɴ ᴄᴏᴏʟᴅᴏᴡɴ)</i></blockquote>"""

    TASK_QUEUED_TXT = """<blockquote>📋 ── <b>ᴛᴀsᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ</b> ── ⏳</blockquote>

🚦 <b>ʙᴏᴛ sʟᴏᴛs ғᴜʟʟ (3/3 ᴀᴄᴛɪᴠᴇ ᴛᴀsᴋs)!</b>
ᴀʟʟ 3 ᴄᴏɴᴄᴜʀʀᴇɴᴛ ᴅᴏᴡɴʟᴏᴀᴅ sʟᴏᴛs ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ ᴏᴄᴄᴜᴘɪᴇᴅ.

📌 <b>ʏᴏᴜʀ ᴛᴀsᴋ ʜᴀs ʙᴇᴇɴ ǫᴜᴇᴜᴇᴅ:</b>
🔢 <b>ᴘᴏsɪᴛɪᴏɴ:</b> <code>#{} ɪɴ ǫᴜᴇᴜᴇ</code>

<blockquote>⚡ <i>ʏᴏᴜʀ ᴛᴀsᴋ ᴡɪʟʟ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ sᴛᴀʀᴛ ᴀs sᴏᴏɴ ᴀs ᴀ sʟᴏᴛ ʙᴇᴄᴏᴍᴇs ғʀᴇᴇ!</i></blockquote>"""

    # --- LOG CHANNEL NOTIFICATIONS (English Small Caps Bold) ---
    LOG_BOT_STARTED_TXT = """📢 <b>[ #ʙᴏᴛ_sᴛᴀʀᴛᴇᴅ ]</b> 🚀

🤖 <b>ʙᴏᴛ ɴᴀᴍᴇ :</b> {bot_name}
🆔 <b>ʙᴏᴛ ᴜsᴇʀɴᴀᴍᴇ :</b> @{bot_username}
👑 <b>ᴏᴡɴᴇʀ :</b> <code>{owner_id}</code>
⚡ <b>ᴍᴀx ᴄᴏɴᴄᴜʀʀᴇɴᴛ ᴛᴀsᴋs :</b> <code>{max_tasks}</code>
⏳ <b>ᴜsᴇʀ ᴄᴏᴏʟᴅᴏᴡɴ :</b> <code>{cooldown}s</code>
🗄️ <b>ᴅᴀᴛᴀʙᴀsᴇ :</b> <code>{db_status}</code>
🕒 <b>sᴛᴀʀᴛᴇᴅ ᴀᴛ :</b> <code>{timestamp}</code>

<blockquote>🌟 <b>ᴇɴɢɪɴᴇ :</b> ᴘʏʀᴏɢʀᴀᴍ ᴍᴛᴘʀᴏᴛᴏ (2ɢʙ sᴜᴘᴘᴏʀᴛ)
🌐 <b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ :</b> <a href='https://t.me/SSBotsUpdates'>★彡 🅂🅂🄱🄾🅃🅂 彡★</a></blockquote>"""

    LOG_NEW_USER_TXT = """👤 <b>[ #ɴᴇᴡ_ᴜsᴇʀ ]</b> 🌺

🆔 <b>ᴜsᴇʀ ɪᴅ :</b> <code>{user_id}</code>
👤 <b>ɴᴀᴍᴇ :</b> <a href='tg://user?id={user_id}'>{name}</a>
🔖 <b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{username}
📊 <b>ᴛᴏᴛᴀʟ ᴜsᴇʀs :</b> <code>{total_users}</code>
🕒 <b>ᴊᴏɪɴᴇᴅ ᴀᴛ :</b> <code>{timestamp}</code>"""

    LOG_NEW_TASK_TXT = """📥 <b>[ #ɴᴇᴡ_ᴛᴀsᴋ ]</b> ⚡

👤 <b>ᴜsᴇʀ :</b> <a href='tg://user?id={user_id}'>{name}</a> (<code>{user_id}</code>)
🌐 <b>sᴏᴜʀᴄᴇ :</b> <code>{provider}</code>
🔗 <b>ᴜʀʟ / ᴛɪᴛʟᴇ :</b> {link_or_title}
🚦 <b>ǫᴜᴇᴜᴇ sᴛᴀᴛᴜs :</b> <code>{queue_status}</code>
🕒 <b>ᴛɪᴍᴇ :</b> <code>{timestamp}</code>"""

    LOG_TASK_COMPLETED_TXT = """✅ <b>[ #ᴛᴀsᴋ_ᴄᴏᴍᴘʟᴇᴛᴇᴅ ]</b> 🚀

👤 <b>ᴜsᴇʀ :</b> <a href='tg://user?id={user_id}'>{name}</a> (<code>{user_id}</code>)
🌐 <b>sᴏᴜʀᴄᴇ :</b> <code>{provider}</code>
📂 <b>ғɪʟᴇ :</b> <code>{file_name}</code>
💾 <b>sɪᴢᴇ :</b> <code>{file_size}</code>
⏱️ <b>ᴛɪᴍᴇ ᴛᴀᴋᴇɴ :</b> <code>{duration}</code>
🕒 <b>ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴀᴛ :</b> <code>{timestamp}</code>"""

    LOG_USER_BANNED_TXT = """🚫 <b>[ #ᴜsᴇʀ_ʙᴀɴɴᴇᴅ ]</b> ⛔

👤 <b>ʙᴀɴɴᴇᴅ ᴜsᴇʀ :</b> <a href='tg://user?id={user_id}'>{name}</a> (<code>{user_id}</code>)
👮 <b>ʙᴀɴɴᴇᴅ ʙʏ :</b> <a href='tg://user?id={admin_id}'>{admin_name}</a> (<code>{admin_id}</code>)
📝 <b>ʀᴇᴀsᴏɴ :</b> <code>{reason}</code>
🕒 <b>ᴛɪᴍᴇ :</b> <code>{timestamp}</code>"""

    LOG_USER_UNBANNED_TXT = """🟢 <b>[ #ᴜsᴇʀ_ᴜɴʙᴀɴɴᴇᴅ ]</b> ✨

👤 <b>ᴜɴʙᴀɴɴᴇᴅ ᴜsᴇʀ :</b> <a href='tg://user?id={user_id}'>{name}</a> (<code>{user_id}</code>)
👮 <b>ᴜɴʙᴀɴɴᴇᴅ ʙʏ :</b> <a href='tg://user?id={admin_id}'>{admin_name}</a> (<code>{admin_id}</code>)
🕒 <b>ᴛɪᴍᴇ :</b> <code>{timestamp}</code>"""

    USER_BANNED_ALERT_TXT = """<blockquote>⛔ ── <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ (ʙᴀɴɴᴇᴅ)</b> ── ⛔</blockquote>

🚫 <b>ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ!</b>
ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀs ʙᴇᴇɴ ʀᴇsᴛʀɪᴄᴛᴇᴅ ʙʏ ᴀɴ ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ.

<blockquote>💬 <i>ɪғ ʏᴏᴜ ʙᴇʟɪᴇᴠᴇ ᴛʜɪs ɪs ᴀ ᴍɪsᴛᴀᴋᴇ, ᴘʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ <a href='https://t.me/Sunil_Sharma_2_0_Bot'>@Sunil_Sharma_2_0_Bot</a></i></blockquote>"""

    # --- ADMIN & SUDO INTERACTION TEXTS ---
    ADMIN_ONLY_TXT = "⛔ <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ :</b> ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ʙᴏᴛ ᴏᴡɴᴇʀ & sᴜᴅᴏ ᴀᴅᴍɪɴs!"
    OWNER_ONLY_TXT = "👑 <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ :</b> ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ʀᴇsᴛʀɪᴄᴛᴇᴅ ᴛᴏ ᴛʜᴇ ʙᴏᴛ ᴏᴡɴᴇʀ ᴏɴʟʏ!"
    BAN_USAGE_TXT = "📖 <b>ᴜsᴀɢᴇ :</b> <code>/ban &lt;user_id&gt; [optional reason]</code> ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴡɪᴛʜ <code>/ban [reason]</code>"
    UNBAN_USAGE_TXT = "📖 <b>ᴜsᴀɢᴇ :</b> <code>/unban &lt;user_id&gt;</code> ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴡɪᴛʜ <code>/unban</code>"
    ADDSUDO_USAGE_TXT = "📖 <b>ᴜsᴀɢᴇ :</b> <code>/addsudo &lt;user_id&gt;</code> ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴡɪᴛʜ <code>/addsudo</code>"
    DELSUDO_USAGE_TXT = "📖 <b>ᴜsᴀɢᴇ :</b> <code>/delsudo &lt;user_id&gt;</code> ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴡɪᴛʜ <code>/delsudo</code>"
    USER_BANNED_SUCCESS = "🚫 <b>ᴜsᴇʀ ʙᴀɴɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!</b>\n\n🆔 <b>ᴜsᴇʀ ɪᴅ :</b> <code>{user_id}</code>\n📝 <b>ʀᴇᴀsᴏɴ :</b> <code>{reason}</code>"
    USER_UNBANNED_SUCCESS = "🟢 <b>ᴜsᴇʀ ᴜɴʙᴀɴɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!</b>\n\n🆔 <b>ᴜsᴇʀ ɪᴅ :</b> <code>{user_id}</code>"
    ALREADY_BANNED = "⚠️ <b>ᴜsᴇʀ <code>{user_id}</code> ɪs ᴀʟʀᴇᴀᴅʏ ʙᴀɴɴᴇᴅ!</b>"
    NOT_BANNED = "⚠️ <b>ᴜsᴇʀ <code>{user_id}</code> ɪs ɴᴏᴛ ʙᴀɴɴᴇᴅ!</b>"
    CANNOT_BAN_ADMIN = "⚠️ <b>ʏᴏᴜ ᴄᴀɴɴᴏᴛ ʙᴀɴ ᴀ sᴜᴅᴏ ᴀᴅᴍɪɴ ᴏʀ ᴛʜᴇ ʙᴏᴛ ᴏᴡɴᴇʀ!</b>"


def get_start_buttons(bot_username: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('📌 ʜᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('💝 ᴀʙᴏᴜᴛ', callback_data='about')
        ],
        [
            InlineKeyboardButton("🛍️ ʟᴏᴏᴛ ᴅᴇᴀʟs 🔥", url=f'https://t.me/{DEALS_CHANNEL}')
        ],
        [
            InlineKeyboardButton("📺 ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ", url=YOUTUBE_URL),
            InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url=CHANNEL_URL)
        ],
        [
            InlineKeyboardButton('🔚 ᴄʟᴏsᴇ', callback_data='close')
        ]
    ])

def get_help_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='home'),
            InlineKeyboardButton('💝 ᴀʙᴏᴜᴛ', callback_data='about')
        ],
        [
            InlineKeyboardButton("🛍️ ʟᴏᴏᴛ ᴅᴇᴀʟs 🔥", url=f'https://t.me/{DEALS_CHANNEL}')
        ],
        [
            InlineKeyboardButton("💬 ᴅᴏᴜʙᴛ / ᴄᴏɴᴛᴀᴄᴛ", url=DEVELOPER_URL)
        ],
        [
            InlineKeyboardButton('🔚 ᴄʟᴏsᴇ', callback_data='close')
        ]
    ])

def get_about_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('📌 ʜᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='home')
        ],
        [
            InlineKeyboardButton("🛍️ ʟᴏᴏᴛ ᴅᴇᴀʟs 🔥", url=f'https://t.me/{DEALS_CHANNEL}')
        ],
        [
            InlineKeyboardButton("📺 ʏᴏᴜᴛᴜʙᴇ", url=YOUTUBE_URL),
            InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url=CHANNEL_URL)
        ],
        [
            InlineKeyboardButton('🔚 ᴄʟᴏsᴇ', callback_data='close')
        ]
    ])

def get_fsub_buttons(updates_invite: str, deals_invite: str, user_id: int):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('📢 1. ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ', url=updates_invite)
        ],
        [
            InlineKeyboardButton('🛍️ 2. ᴊᴏɪɴ ᴅᴇᴀʟs ᴄʜᴀɴɴᴇʟ 🔥', url=deals_invite)
        ],
        [
            InlineKeyboardButton('✅ ᴠᴇʀɪғʏ & sᴛᴀʀᴛ', callback_data=f'verify_{user_id}')
        ]
    ])

def get_youtube_quality_buttons(cache_id: str, download_links: list):
    """Builds clean inline buttons for each YouTube quality option"""
    buttons = []
    video_row = []
    audio_row = []

    for idx, item in enumerate(download_links):
        fmt = str(item.get("format") or "")
        label = item.get("label") or fmt
        itype = item.get("type") or "video"

        if fmt in ["1080", "1080p"]:
            btn_text = "🎬 1080ᴘ ᴍᴘ4"
        elif fmt in ["720", "720p"]:
            btn_text = "🎬 720ᴘ ᴍᴘ4"
        elif fmt in ["480", "480p"]:
            btn_text = "🎬 480ᴘ ᴍᴘ4"
        elif fmt in ["360", "360p"]:
            btn_text = "🎬 360ᴘ ᴍᴘ4"
        elif fmt in ["240", "240p"]:
            btn_text = "🎬 240ᴘ ᴍᴘ4"
        elif fmt in ["144", "144p"]:
            btn_text = "🎬 144ᴘ ᴍᴘ4"
        elif fmt in ["4k", "2160"]:
            btn_text = "🎬 4ᴋ (2160ᴘ)"
        elif fmt in ["1440"]:
            btn_text = "🎬 2ᴋ (1440ᴘ)"
        elif fmt.lower() == "mp3":
            btn_text = "🎵 ᴍᴘ3 ᴀᴜᴅɪᴏ"
        elif fmt.lower() == "m4a":
            btn_text = "🎵 ᴍ4ᴀ ᴀᴜᴅɪᴏ"
        elif fmt.lower() == "flac":
            btn_text = "🎵 ғʟᴀᴄ ᴀᴜᴅɪᴏ"
        else:
            btn_text = f"📦 {fmt.upper()}"

        cb_data = f"ytq:{cache_id}:{idx}"

        if itype == "audio":
            audio_row.append(InlineKeyboardButton(btn_text, callback_data=cb_data))
        else:
            video_row.append(InlineKeyboardButton(btn_text, callback_data=cb_data))

    for i in range(0, len(video_row), 2):
        buttons.append(video_row[i:i+2])

    for i in range(0, len(audio_row), 2):
        buttons.append(audio_row[i:i+2])

    buttons.append([InlineKeyboardButton("🔚 ᴄʟᴏsᴇ", callback_data="close")])
    return InlineKeyboardMarkup(buttons)
