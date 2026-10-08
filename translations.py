# ==============================================================================
# 🤖 Bot Developer / Owner : Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ
# 🌐 Developer URL        : https://t.me/Sunil_Sharma_2_0_Bot (@Sunil_Sharma_2_0_Bot)
# 📢 Telegram Channel     : https://t.me/SSBotsUpdates (@SSBotsUpdates)
# 📺 YouTube Channel      : https://www.youtube.com/@SunilWebTricks (SunilWebTricks)
# 💬 Ask Doubt / Contact   : @Sunil_Sharma_2_0_Bot
# ==============================================================================

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

class Script:
    START_TXT = """<blockquote><b>👋 𝐇ᴇʟʟᴏ {} ! 🌺</b></blockquote>

🤖 <b>𝐈 𝐀ᴍ 𝐓ʜᴇ 𝐅ᴀsᴛᴇsᴛ 𝐓ᴇʀᴀ𝐁ᴏx & 𝐃ɪsᴋᴡᴀʟᴀ 𝐃ᴏᴡɴʟᴏᴀᴅᴇʀ 𝐁ᴏᴛ ⚡</b>

📁 <b>𝐒ᴇɴᴅ 𝐌ᴇ 𝐀ɴʏ 𝐓ᴇʀᴀ𝐁ᴏx 𝐎ʀ 𝐃ɪsᴋᴡᴀʟᴀ 𝐋ɪɴᴋ, 𝐈 𝐖ɪʟʟ :</b>
• 🔍 <b>𝐈ɴsᴛᴀɴᴛʟʏ 𝐃ᴇᴛᴇᴄᴛ & 𝐄xᴛʀᴀᴄᴛ 𝐓ʜᴇ 𝐅ɪʟᴇ</b>
• ⏬ <b>𝐃ᴏᴡɴʟᴏᴀᴅ 𝐀ᴛ 𝐔ʟᴛʀᴀ 𝐇ɪɢʜ 𝐒ᴘᴇᴇᴅ</b>
• 📤 <b>𝐔ᴘʟᴏᴀᴅ 𝐃ɪʀᴇᴄᴛʟʏ 𝐓ᴏ 𝐓ᴇʟᴇɢʀᴀᴍ (𝐔ᴘ 𝐓ᴏ 𝟐𝐆𝐁) 🚀</b>

━༻« ★ <b>𝐒ᴘᴇᴄɪᴀʟ 𝐅ᴇᴀᴛᴜʀᴇs</b> ★ »༺━
<blockquote>• <b>𝐔ɴʟɪᴍɪᴛᴇᴅ 𝟐𝐆𝐁 𝐌𝐓𝐏ʀᴏᴛᴏ 𝐔ᴘʟᴏᴀᴅs</b> 
• <b>𝐒ᴜᴘᴘᴏʀᴛs 𝐀ʟʟ 𝟐𝟎+ 𝐓ᴇʀᴀ𝐁ᴏx 𝐌ɪʀʀᴏʀ 𝐃ᴏᴍᴀɪɴs</b>
• <b>𝐃ɪsᴋᴡᴀʟᴀ 𝐕ɪᴅᴇᴏ 𝐒ᴛʀᴇᴀᴍ 𝐃ᴏᴡɴʟᴏᴀᴅᴇʀ</b>
• <b>𝐋ɪᴠᴇ 𝐃ᴏᴡɴʟᴏᴀᴅ & 𝐔ᴘʟᴏᴀᴅ 𝐏ʀᴏɢʀᴇss 𝐁ᴀʀs</b></blockquote>

⭐ <b>𝐏ᴏᴡᴇʀᴇᴅ 𝐁ʏ <a href='https://t.me/SSBotsUpdates'>★彡 🅂🅂🄱🄾🅃🅂 彡★</a></b>"""

    HELP_TXT = """<blockquote><b>📘 ── 𝐇ᴇʟᴘ & 𝐔sᴀɢᴇ 𝐆ᴜɪᴅᴇ ── 📖</b></blockquote>

💫 <b>𝐇ᴏᴡ 𝐓ᴏ 𝐃ᴏᴡɴʟᴏᴀᴅ & 𝐑ᴇᴄᴇɪᴠᴇ 𝐅ɪʟᴇs :</b>

🚀 <b>𝐒ᴛᴇᴘ 𝟏 : 𝐒ᴇɴᴅ 𝐋ɪɴᴋ</b>
<blockquote>• 𝐂ᴏᴘʏ 𝐚𝐧𝐲 <b>𝐓ᴇʀᴀ𝐁ᴏx</b> (terabox.com, terabox.app, 1024terabox.com, etc.) 𝐨𝐫 <b>𝐃ɪsᴋᴡᴀʟᴀ</b> link.
• 𝐏ᴀsᴛᴇ 𝐢𝐭 𝐝ɪʀᴇ𝐜ᴛ𝐥𝐲 𝐢𝐧 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭.</blockquote>

⚡ <b>𝐒ᴛᴇᴘ 𝟐 : 𝐀ᴜᴛᴏ-𝐃ᴏᴡɴʟᴏᴀᴅ</b>
<blockquote>• 𝐁ᴏᴛ 𝐰𝐢𝐥𝐥 𝐢𝐧𝐬𝐭𝐚𝐧𝐭𝐥𝐲 𝐝𝐞𝐭𝐞𝐜𝐭 𝐭𝐡𝐞 𝐥𝐢𝐧𝐤.
• 𝐅𝐢𝐥𝐞 𝐰𝐢𝐥𝐥 𝐛𝐞 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐝 𝐰𝐢𝐭𝐡 𝐚 𝐥𝐢𝐯𝐞 𝐬𝐩𝐞𝐞𝐝 𝐩𝐫𝐨𝐠𝐫𝐞𝐬𝐬 𝐛𝐚𝐫.</blockquote>

📤 <b>𝐒ᴛᴇᴘ 𝟑 : 𝐓ᴇʟᴇɢʀᴀᴍ 𝐔ᴘʟᴏᴀᴅ</b>
<blockquote>• 𝐁ᴏᴛ 𝐰𝐢𝐥𝐥 𝐮𝐩𝐥𝐨𝐚𝐝 𝐭𝐡𝐞 𝐯𝐢𝐝𝐞𝐨/𝐝𝐨𝐜𝐮𝐦𝐞𝐧𝐭 𝐝𝐢𝐫𝐞𝐜𝐭𝐥𝐲 𝐭𝐨 𝐲𝐨𝐮 (𝐮𝐩 𝐭𝐨 <b>𝟐 𝐆𝐁</b>).
• 𝐕𝐢𝐝𝐞𝐨𝐬 𝐚𝐫𝐞 𝐬𝐞𝐧𝐭 𝐰𝐢𝐭𝐡 𝐬𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠 𝐬𝐮𝐩𝐩𝐨𝐫𝐭!</blockquote>

<b><blockquote>⚠️ 𝐑ᴇᴘᴏʀᴛ 𝐈ssᴜᴇ: <a href='https://t.me/Sunil_Sharma_2_0_Bot'>𓆩Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ [🇳🇵]𓆪</a></b></blockquote>"""

    ABOUT_TXT = """<blockquote><b>🌟 ── 𝐀ʙᴏᴜᴛ 𝐌ᴇ • 𝐃ᴏᴡɴʟᴏᴀᴅᴇʀ ── 🌟</b></blockquote>

📌 <b>𝐈 𝐀ᴍ 𝐘ᴏᴜʀ 𝐔ʟᴛɪᴍᴀᴛᴇ 𝐓ᴇʀᴀ𝐁ᴏx & 𝐃ɪsᴋᴡᴀʟᴀ 𝐂ʟᴏᴜᴅ 𝐃ᴏᴡɴʟᴏᴀᴅᴇʀ ⚡</b>

‣ <b>𝐌ʏ 𝐍ᴀᴍᴇ :</b> <a href="https://t.me/{}">{}</a>
‣ <b>𝐃ᴇᴠᴇʟᴏᴘᴇʀ :</b> <a href="https://t.me/Sunil_Sharma_2_0_Bot">𓆩Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ [🇳🇵]𓆪</a>
‣ <b>𝐔ᴘᴅᴀᴛᴇs 𝐂ʜᴀɴɴᴇʟ :</b> <a href="https://t.me/SSBotsUpdates">𝐒𝐒 𝐁ᴏᴛs 𝐔ᴘᴅᴀᴛᴇs</a>
‣ <b>𝐘ᴏᴜ𝐓ᴜʙᴇ 𝐂ʜᴀɴɴᴇʟ :</b> <a href="https://www.youtube.com/@SunilWebTricks">SunilWebTricks</a>
‣ <b>𝐋ᴀɴɢᴜᴀɢᴇ :</b> <a href="https://www.python.org/">𝐏ʏᴛʜᴏɴ 3.11+</a>
‣ <b>𝐅ʀᴀᴍᴇᴡᴏʀᴋ :</b> <a href="https://docs.pyrogram.org/">𝐏ʏʀᴏɢʀᴀᴍ &amp; 𝐓ɢ𝐂ʀʏᴘᴛᴏ</a>
‣ <b>𝐔ᴘʟᴏᴀᴅ 𝐋ɪᴍɪᴛ :</b> <code>𝟐,𝟎𝟒𝟖 𝐌𝐁 (𝟐 𝐆𝐁 𝐌𝐓𝐏ʀᴏᴛᴏ)</code>
‣ <b>𝐁ᴜɪʟᴅ 𝐒ᴛᴀᴛᴜs :</b> <code>v3.2.0 [ 𝐒ᴛᴀʙʟᴇ &amp; 𝐎ᴘᴛɪᴍɪᴢᴇᴅ ]</code>

<i>💖 𝗜ꜰ 𝗬ᴏᴜ 𝗙ɪɴᴅ 𝗠ᴇ 𝗨ꜱᴇꜰᴜʟ, 𝗣ʟᴇᴀꜱᴇ 𝗖ᴏɴꜱɪᴅᴇʀ 𝗦ʜᴀʀɪɴɢ 𝗠ᴇ 𝗪ɪᴛʜ 𝗬ᴏᴜʀ 𝗙ʀɪᴇɴᴅꜱ!</i>"""

    FORCE_SUB_TXT = """<blockquote><b>🔐 ── 𝐕ᴇʀɪғɪᴄᴀᴛɪᴏɴ 𝐑ᴇǫᴜɪʀᴇᴅ ── 🔐</b></blockquote>

👋 <b>𝐇ᴇʟʟᴏ {} ! 🌺</b>

😇 <b>𝐘ᴏᴜ 𝐌ᴜsᴛ 𝐉ᴏɪɴ 𝐁ᴏᴛʜ 𝐎ᴜʀ 𝐂ʜᴀɴɴᴇʟs 𝐓ᴏ 𝐔sᴇ 𝐓ʜɪs 𝐁ᴏᴛ :</b>

📢 <b>𝟏. 𝐁ᴏᴛ 𝐔ᴘᴅᴀᴛᴇs 𝐂ʜᴀɴɴᴇʟ</b>
🛍️ <b>𝟐. 𝐋ᴏᴏᴛ 𝐃ᴇᴀʟs 𝐂ʜᴀɴɴᴇʟ</b>

👉 <i>𝐂ʟɪᴄᴋ 𝐁ᴏᴛ𝐡 ‘𝐉ᴏɪɴ’ 𝐁ᴜᴛᴛᴏɴs 𝐁ᴇʟᴏᴡ, 𝐓ʜᴇɴ 𝐏ʀᴇss ‘✅ 𝐕ᴇʀɪғʏ’ 𝐓ᴏ 𝐔ɴʟᴏᴄᴋ!</i>"""

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
            InlineKeyboardButton("🛍️ 𝐋ᴏᴏᴛ 𝐃ᴇᴀʟs 🔥", url=f'https://t.me/{config.DEALS_CHANNEL}')
        ],
        [
            InlineKeyboardButton("📺 𝐘ᴏᴜ𝐓ᴜʙᴇ 𝐂ʜᴀɴɴᴇʟ", url=config.YOUTUBE_URL),
            InlineKeyboardButton("📢 𝐔ᴘᴅᴀᴛᴇs", url=config.CHANNEL_URL)
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
            InlineKeyboardButton("🛍️ 𝐋ᴏᴏᴛ 𝐃ᴇᴀʟs 🔥", url=f'https://t.me/{config.DEALS_CHANNEL}')
        ],
        [
            InlineKeyboardButton("💬 𝐃ᴏᴜʙᴛ / 𝐂ᴏɴᴛᴀᴄᴛ", url=config.DEVELOPER_URL)
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
            InlineKeyboardButton("🛍️ 𝐋ᴏᴏᴛ 𝐃ᴇᴀʟs 🔥", url=f'https://t.me/{config.DEALS_CHANNEL}')
        ],
        [
            InlineKeyboardButton("📺 𝐘ᴏᴜ𝐓ᴜʙᴇ", url=config.YOUTUBE_URL),
            InlineKeyboardButton("📢 𝐔ᴘᴅᴀᴛᴇs", url=config.CHANNEL_URL)
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
