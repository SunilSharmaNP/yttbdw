# ==============================================================================
# 🤖 Bot Developer / Owner : Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ
# 🌐 Developer URL        : https://t.me/Sunil_Sharma_2_0_Bot (@Sunil_Sharma_2_0_Bot)
# 📢 Telegram Channel     : https://t.me/SSBotsUpdates (@SSBotsUpdates)
# 📺 YouTube Channel      : https://www.youtube.com/@SunilWebTricks (SunilWebTricks)
# 💬 Ask Doubt / Contact   : @Sunil_Sharma_2_0_Bot
# ==============================================================================

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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

class Script:
    START_TXT = """<blockquote><b>👋 𝐇ᴇʟʟᴏ {} ! 🌺</b></blockquote>

🤖 <b>𝐈 𝐀ᴍ 𝐓ʜᴇ 𝐅ᴀsᴛᴇsᴛ 𝐓ᴇʀᴀ𝐁ᴏx, 𝐃ɪsᴋᴡᴀʟᴀ & 𝐘ᴏᴜ𝐓ᴜʙᴇ 𝐃ᴏᴡɴʟᴏᴀᴅᴇʀ ⚡</b>

📁 <b>𝐒ᴇɴᴅ 𝐌ᴇ 𝐀ɴʏ 𝐒ᴜᴘᴘᴏʀᴛᴇᴅ 𝐋ɪɴᴋ, 𝐈 𝐖ɪʟʟ :</b>
• 🔍 <b>𝐈ɴsᴛᴀɴᴛʟʏ 𝐃ᴇᴛᴇᴄᴛ & 𝐄xᴛʀᴀᴄᴛ 𝐓ʜᴇ 𝐅ɪʟᴇ</b>
• ⏬ <b>𝐃ᴏᴡɴʟᴏᴀᴅ 𝐀ᴛ 𝐔ʟᴛʀᴀ 𝐇ɪɢʜ 𝐒ᴘᴇᴇᴅ</b>
• 📤 <b>𝐔ᴘʟᴏᴀᴅ 𝐃ɪʀᴇᴄᴛʟʏ 𝐓ᴏ 𝐓ᴇʟᴇɢʀᴀᴍ (𝐔ᴘ 𝐓ᴏ 𝟐𝐆𝐁) 🚀</b>

━༻« ★ <b>𝐒ᴘᴇᴄɪᴀʟ 𝐅ᴇᴀᴛᴜʀᴇs</b> ★ »༺━
<blockquote>• <b>𝐔ɴʟɪᴍɪᴛᴇᴅ 𝟐𝐆𝐁 𝐌𝐓𝐏ʀᴏᴛᴏ 𝐔ᴘʟᴏᴀᴅs</b> 
• <b>𝐒ᴜᴘᴘᴏʀᴛs 𝐀ʟʟ 𝟐𝟎+ 𝐓ᴇʀᴀ𝐁ᴏx 𝐌ɪʀʀᴏʀ 𝐃ᴏᴍᴀɪɴs</b>
• <b>𝐘ᴏᴜ𝐓ᴜʙᴇ 𝐕ɪᴅᴇᴏ (𝟑𝟔𝟎𝐩, 𝟕𝟐𝟎𝐩, 𝟏𝟎𝟖𝟎𝐩) & 𝐌𝐏𝟑 𝐀ᴜᴅɪᴏ</b>
• <b>𝐃ɪsᴋᴡᴀʟᴀ 𝐕ɪᴅᴇᴏ 𝐒ᴛʀᴇᴀᴍ 𝐃ᴏᴡɴʟᴏᴀᴅᴇʀ</b>
• <b>𝐋ɪᴠᴇ 𝐃ᴏᴡɴʟᴏᴀᴅ & 𝐔ᴘʟᴏᴀᴅ 𝐏ʀᴏɢʀᴇss 𝐁ᴀʀs</b></blockquote>

⭐ <b>𝐏ᴏᴡᴇʀᴇᴅ 𝐁ʏ <a href='https://t.me/SSBotsUpdates'>★彡 🅂🅂🄱🄾🅃🅂 彡★</a></b>"""

    HELP_TXT = """<blockquote><b>📘 ── 𝐇ᴇʟᴘ & 𝐔sᴀɢᴇ 𝐆ᴜɪᴅᴇ ── 📖</b></blockquote>

💫 <b>𝐇ᴏᴡ 𝐓ᴏ 𝐃ᴏᴡɴʟᴏᴀᴅ & 𝐑ᴇᴄᴇɪᴠᴇ 𝐅ɪʟᴇs :</b>

🚀 <b>𝐒ᴛᴇᴘ 𝟏 : 𝐒ᴇɴᴅ 𝐋ɪɴᴋ</b>
<blockquote>• 𝐂ᴏᴘʏ 𝐚ɴ𝐲 <b>𝐓ᴇʀᴀ𝐁ᴏx</b> (terabox.com, 1024terabox.com, etc.), <b>𝐘ᴏᴜ𝐓ᴜʙᴇ</b>, 𝐨𝐫 <b>𝐃ɪsᴋᴡᴀʟᴀ</b> 𝐥𝐢𝐧𝐤.
• 𝐏ᴀsᴛᴇ 𝐢𝐭 𝐝ɪʀᴇ𝐜ᴛʟ𝐲 𝐢𝐧 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭.</blockquote>

⚡ <b>𝐒ᴛᴇᴘ 𝟐 : 𝐐ᴜᴀʟɪᴛʏ 𝐒ᴇʟᴇᴄᴛɪᴏɴ (𝐅ᴏʀ 𝐘ᴏᴜ𝐓ᴜʙᴇ)</b>
<blockquote>• 𝐅𝐨𝐫 𝐘𝐨𝐮𝐓𝐮𝐛𝐞, 𝐭𝐡𝐞 𝐛𝐨𝐭 𝐰𝐢𝐥𝐥 𝐟𝐞𝐭𝐜𝐡 𝐚𝐥𝐥 𝐯𝐢𝐝𝐞𝐨 (𝟏𝟎𝟖𝟎𝐩, 𝟕𝟐𝟎𝐩, 𝟒𝟖𝟎𝐩, 𝟑𝟔𝟎𝐩) & 𝐌𝐏𝟑 𝐪𝐮𝐚𝐥𝐢𝐭𝐢𝐞𝐬.
• 𝐓𝐚𝐩 𝐲𝐨𝐮𝐫 𝐝𝐞𝐬𝐢𝐫𝐞𝐝 𝐪𝐮𝐚𝐥𝐢𝐭𝐲 𝐛𝐮𝐭𝐭𝐨𝐧!</blockquote>

📤 <b>𝐒ᴛᴇᴘ 𝟑 : 𝐓ᴇʟᴇɢʀᴀᴍ 𝐔ᴘʟᴏᴀᴅ</b>
<blockquote>• 𝐁ᴏ𝐭 𝐰𝐢𝐥𝐥 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐚𝐧𝐝 𝐮𝐩𝐥𝐨𝐚𝐝 𝐭𝐡𝐞 𝐯𝐢𝐝𝐞𝐨/𝐝𝐨𝐜𝐮𝐦𝐞𝐧𝐭 𝐝𝐢𝐫ᴇ𝐜ᴛ𝐥𝐲 𝐭𝐨 𝐲𝐨𝐮 (𝐮𝐩 𝐭𝐨 <b>𝟐 𝐆𝐁</b>).
• 𝐕𝐢𝐝𝐞𝐨𝐬 𝐚𝐫𝐞 𝐬𝐞𝐧𝐭 𝐰𝐢𝐭𝐡 𝐬𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠 𝐬𝐮𝐩𝐩𝐨𝐫𝐭!</blockquote>

<b><blockquote>⚠️ 𝐑ᴇᴘᴏʀᴛ 𝐈ssᴜᴇ: <a href='https://t.me/Sunil_Sharma_2_0_Bot'>𓆩Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ [🇳🇵]𓆪</a></b></blockquote>"""

    ABOUT_TXT = """<blockquote><b>🌟 ── 𝐀ʙᴏᴜᴛ 𝐌ᴇ • 𝐃ᴏᴡɴʟᴏᴀᴅᴇʀ ── 🌟</b></blockquote>

📌 <b>𝐈 𝐀ᴍ 𝐘ᴏᴜʀ 𝐔ʟᴛɪᴍᴀ𝐓ᴇ 𝐓ᴇʀᴀ𝐁ᴏx, 𝐃ɪsᴋᴡᴀʟᴀ & 𝐘ᴏᴜ𝐓ᴜʙᴇ 𝐃ᴏᴡɴʟᴏᴀᴅᴇʀ ⚡</b>

‣ <b>𝐌ʏ 𝐍ᴀᴍᴇ :</b> <a href="https://t.me/{}">{}</a>
‣ <b>𝐃ᴇᴠᴇʟᴏᴘᴇʀ :</b> <a href="https://t.me/Sunil_Sharma_2_0_Bot">𓆩Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ [🇳🇵]𓆪</a>
‣ <b>𝐔ᴘᴅᴀᴛᴇs 𝐂ʜᴀɴɴᴇʟ :</b> <a href="https://t.me/SSBotsUpdates">𝐒𝐒 𝐁ᴏᴛs 𝐔ᴘᴅᴀᴛᴇs</a>
‣ <b>𝐘ᴏᴜ𝐓ᴜʙᴇ 𝐂ʜᴀɴɴᴇʟ :</b> <a href="https://www.youtube.com/@SunilWebTricks">SunilWebTricks</a>
‣ <b>𝐋ᴀɴɢᴜᴀɢᴇ :</b> <a href="https://www.python.org/">𝐏ʏᴛʜᴏɴ 3.11+</a>
‣ <b>𝐅ʀᴀᴍᴇᴡᴏʀᴋ :</b> <a href="https://docs.pyrogram.org/">𝐏ʏʀᴏɢʀᴀᴍ &amp; 𝐓ɢ𝐂ʀʏᴘᴛᴏ</a>
‣ <b>𝐔ᴘʟᴏᴀᴅ 𝐋ɪᴍɪᴛ :</b> <code>𝟐,𝟎𝟒𝟖 𝐌𝐁 (𝟐 𝐆𝐁 𝐌𝐓𝐏ʀᴏᴛᴏ)</code>
‣ <b>𝐁ᴜɪʟᴅ 𝐒ᴛᴀᴛᴜs :</b> <code>v3.5.0 [ 𝐒ᴛᴀʙʟᴇ &amp; 𝐎ᴘᴛɪᴍɪᴢᴇᴅ ]</code>

<i>💖 𝗜ꜰ 𝗬ᴏᴜ 𝗙ɪɴᴅ 𝗠ᴇ 𝗨ꜱᴇꜰᴜʟ, 𝗣ʟᴇᴀꜱᴇ 𝗖ᴏɴꜱɪᴅᴇʀ 𝗦ʜᴀʀɪɴɢ 𝗠ᴇ 𝗪ɪᴛʜ 𝗬ᴏᴜʀ 𝗙ʀɪᴇɴᴅꜱ!</i>"""

    FORCE_SUB_TXT = """<blockquote><b>🔐 ── 𝐕ᴇʀɪғɪᴄᴀᴛɪᴏɴ 𝐑ᴇǫᴜɪʀᴇᴅ ── 🔐</b></blockquote>

👋 <b>𝐇ᴇʟʟᴏ {} ! 🌺</b>

😇 <b>𝐘ᴏᴜ 𝐌ᴜsᴛ 𝐉ᴏɪɴ 𝐁ᴏᴛʜ 𝐎ᴜʀ 𝐂ʜᴀɴɴᴇʟs 𝐓ᴏ 𝐔sᴇ 𝐓ʜɪs 𝐁ᴏᴛ :</b>

📢 <b>𝟏. 𝐁ᴏᴛ 𝐔ᴘᴅᴀᴛᴇs 𝐂ʜᴀɴɴᴇʟ</b>
🛍️ <b>𝟐. 𝐋ᴏᴏᴛ 𝐃ᴇᴀʟs 𝐂ʜᴀɴɴᴇʟ</b>

👉 <i>𝐂ʟɪᴄᴋ 𝐁ᴏᴛ𝐡 ‘𝐉ᴏɪɴ’ 𝐁ᴜᴛᴛᴏɴs 𝐁ᴇʟᴏᴡ, 𝐓ʜᴇɴ 𝐏ʀᴇss ‘✅ 𝐕ᴇʀɪғʏ’ 𝐓ᴏ 𝐔ɴʟᴏᴄᴋ!</i>"""

    YT_WAIT_TXT = """<blockquote><b>⏳ ── 𝐄xᴛʀᴀᴄᴛɪɴɢ 𝐘ᴏᴜ𝐓ᴜʙᴇ 𝐐ᴜᴀʟɪᴛɪᴇs ── 🎬</b></blockquote>

🔍 <b>𝐋ᴏᴀᴅɪɴɢ 𝐀ʟʟ 𝐕ɪᴅᴇᴏ & 𝐀ᴜᴅɪᴏ 𝐅ᴏʀᴍᴀᴛs...</b>

<blockquote>⚡ <i>𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝟒𝟎-𝟓𝟎 𝐬𝐞𝐜𝐨𝐧𝐝𝐬. 𝐎𝐮𝐫 𝐡𝐢𝐠𝐡-𝐬𝐩𝐞𝐞𝐝 𝐞𝐧𝐠𝐢𝐧𝐞 𝐢𝐬 𝐞𝐱𝐭𝐫𝐚𝐜𝐭𝐢𝐧𝐠 𝐚𝐥𝐥 𝐯𝐞𝐫𝐢𝐟𝐢𝐞𝐝 𝐪𝐮𝐚𝐥𝐢𝐭𝐢𝐞𝐬 (𝟏𝟎𝟖𝟎𝐩, 𝟕𝟐𝟎𝐩, 𝟒𝟖𝟎𝐩, 𝟑𝟔𝟎𝐩 &amp; 𝐌𝐏𝟑)...</i></blockquote>"""

    YT_INFO_TXT = """<blockquote><b>🎬 ── 𝐘ᴏᴜ𝐓ᴜʙᴇ 𝐃ᴏᴡɴʟᴏᴀᴅᴇʀ ── 🎬</b></blockquote>

📌 <b>𝐓ɪᴛʟᴇ :</b> <code>{title}</code>
👤 <b>𝐂ʜᴀɴɴᴇʟ :</b> <code>{author}</code>

👇 <b>𝐒ᴇʟᴇᴄᴛ 𝐀 𝐐ᴜᴀʟɪᴛʏ 𝐁ᴇʟᴏᴡ 𝐓ᴏ 𝐃ᴏᴡɴʟᴏᴀᴅ & 𝐔ᴘʟᴏᴀᴅ :</b>"""

    CAPTION_TXT = """<b>📂 𝐅ɪʟᴇɴᴀᴍᴇ :</b> <code>{file_name}</code>
💾 <b>𝐅ɪʟᴇ 𝐒ɪᴢᴇ :</b> <code>{file_size}</code>
🌐 <b>𝐒ᴏᴜʀᴄᴇ :</b> <code>{provider}</code>

♻️ <b>𝐅ᴏʀ 𝐋ᴏᴏᴛ 𝐃ᴇᴀʟs 𝐎ғғᴇʀs 🔥</b>
📌 <b>𝐉ᴏɪɴ :</b> @{deals_channel}

<blockquote>⚡ <b>𝐔ᴘʟᴏᴀᴅᴇᴅ 𝐁ʏ <a href='https://t.me/SSBotsUpdates'>★彡 🅂🅂🄱🄾🅃🅂 彡★</a> • 𝟐𝐆𝐁 𝐌𝐓𝐏ʀᴏᴛᴏ</b></blockquote>"""


def get_start_buttons(bot_username: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('📌 𝐇ᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('💝 𝐀ʙᴏᴜᴛ', callback_data='about')
        ],
        [
            InlineKeyboardButton("🛍️ 𝐋ᴏᴏᴛ 𝐃ᴇᴀʟs 🔥", url=f'https://t.me/{DEALS_CHANNEL}')
        ],
        [
            InlineKeyboardButton("📺 𝐘ᴏᴜ𝐓ᴜʙᴇ 𝐂ʜᴀɴɴᴇʟ", url=YOUTUBE_URL),
            InlineKeyboardButton("📢 𝐔ᴘᴅᴀᴛᴇs", url=CHANNEL_URL)
        ],
        [
            InlineKeyboardButton('🔚 𝐂ʟᴏsᴇ 🔚', callback_data='close')
        ]
    ])

def get_help_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('🏠 𝐇ᴏᴍᴇ', callback_data='home'),
            InlineKeyboardButton('💝 𝐀ʙᴏᴜᴛ', callback_data='about')
        ],
        [
            InlineKeyboardButton("🛍️ 𝐋ᴏᴏᴛ 𝐃ᴇᴀʟs 🔥", url=f'https://t.me/{DEALS_CHANNEL}')
        ],
        [
            InlineKeyboardButton("💬 𝐃ᴏᴜʙᴛ / 𝐂ᴏɴᴛᴀᴄᴛ", url=DEVELOPER_URL)
        ],
        [
            InlineKeyboardButton('🔚 𝐂ʟᴏsᴇ 🔚', callback_data='close')
        ]
    ])

def get_about_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('📌 𝐇ᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('🏠 𝐇ᴏᴍᴇ', callback_data='home')
        ],
        [
            InlineKeyboardButton("🛍️ 𝐋ᴏᴏᴛ 𝐃ᴇᴀʟs 🔥", url=f'https://t.me/{DEALS_CHANNEL}')
        ],
        [
            InlineKeyboardButton("📺 𝐘ᴏᴜ𝐓ᴜʙᴇ", url=YOUTUBE_URL),
            InlineKeyboardButton("📢 𝐔ᴘᴅᴀᴛᴇs", url=CHANNEL_URL)
        ],
        [
            InlineKeyboardButton('🔚 𝐂ʟᴏsᴇ 🔚', callback_data='close')
        ]
    ])

def get_fsub_buttons(updates_invite: str, deals_invite: str, user_id: int):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('📢 𝟏. 𝐉ᴏɪɴ 𝐔ᴘᴅᴀᴛᴇs 𝐂ʜᴀɴɴᴇʟ', url=updates_invite)
        ],
        [
            InlineKeyboardButton('🛍️ 𝟐. 𝐉ᴏɪɴ 𝐃ᴇᴀʟs 𝐂ʜᴀɴɴᴇʟ 🔥', url=deals_invite)
        ],
        [
            InlineKeyboardButton('✅ 𝐕ᴇʀɪғʏ & 𝐒ᴛᴀʀᴛ', callback_data=f'verify_{user_id}')
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
            btn_text = "🎬 1080p MP4"
        elif fmt in ["720", "720p"]:
            btn_text = "🎬 720p MP4"
        elif fmt in ["480", "480p"]:
            btn_text = "🎬 480p MP4"
        elif fmt in ["360", "360p"]:
            btn_text = "🎬 360p MP4"
        elif fmt in ["4k", "2160"]:
            btn_text = "🎬 4K (2160p)"
        elif fmt in ["1440"]:
            btn_text = "🎬 2K (1440p)"
        elif fmt.lower() == "mp3":
            btn_text = "🎵 MP3 Audio"
        elif fmt.lower() == "m4a":
            btn_text = "🎵 M4A Audio"
        elif fmt.lower() == "flac":
            btn_text = "🎵 FLAC Audio"
        else:
            btn_text = f"📦 {fmt.upper()}"

        cb_data = f"ytq_{cache_id}_{idx}"

        if itype == "audio":
            audio_row.append(InlineKeyboardButton(btn_text, callback_data=cb_data))
        else:
            video_row.append(InlineKeyboardButton(btn_text, callback_data=cb_data))

    for i in range(0, len(video_row), 2):
        buttons.append(video_row[i:i+2])

    for i in range(0, len(audio_row), 2):
        buttons.append(audio_row[i:i+2])

    buttons.append([InlineKeyboardButton("🔚 𝐂ʟᴏsᴇ", callback_data="close")])
    return InlineKeyboardMarkup(buttons)
