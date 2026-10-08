<!--
==============================================================================
🤖 Bot Developer / Owner : Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ
🌐 Developer URL        : https://t.me/Sunil_Sharma_2_0_Bot (@Sunil_Sharma_2_0_Bot)
📢 Telegram Channel     : https://t.me/SSBotsUpdates (@SSBotsUpdates)
📺 YouTube Channel      : https://www.youtube.com/@SunilWebTricks (SunilWebTricks)
💬 Ask Doubt / Contact   : @Sunil_Sharma_2_0_Bot
==============================================================================
-->

# 🚀 TeraBox, Diskwala & YouTube Downloader Bot (Pyrogram MTProto)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Framework-Pyrogram%20MTProto-purple.svg" alt="Pyrogram">
  <img src="https://img.shields.io/badge/Upload%20Cap-2%20GB%20MTProto-success.svg" alt="2GB Uploads">
  <img src="https://img.shields.io/badge/API-Sunil--SSBots%20Vercel%20Engine-cyan.svg" alt="API Engine">
  <img src="https://img.shields.io/badge/Developer-Ꞩᵾꞥīł%20Ꞩħⱥɍᵯⱥ%20ƻ.Ꝋ-orange.svg" alt="Developer">
</p>

An ultra-fast, professional Telegram Bot built with **Python & Pyrogram (MTProto)** and powered by **Sunil-SSBots High-Speed API Engine** (`https://sunil-ssbots.vercel.app`).

---

## 👤 Developer & Community

| 🏷️ Field | 🔗 Link / Details |
| :--- | :--- |
| **🤖 Developer / Owner** | **Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ** ([@Sunil_Sharma_2_0_Bot](https://t.me/Sunil_Sharma_2_0_Bot)) |
| **📢 Telegram Channel** | [★彡 🅂🅂🄱🄾🅃🅂 彡★ (@SSBotsUpdates)](https://t.me/SSBotsUpdates) |
| **🛍️ Loot Deals Channel** | [@Tg_Shoping](https://t.me/Tg_Shoping) |
| **📺 YouTube Channel** | [SunilWebTricks (@SunilWebTricks)](https://www.youtube.com/@SunilWebTricks) |
| **💬 Ask Doubt / Support** | [@Sunil_Sharma_2_0_Bot](https://t.me/Sunil_Sharma_2_0_Bot) |
| **🌐 API Engine** | [sunil-ssbots.vercel.app](https://sunil-ssbots.vercel.app) |

---

## ✨ Features & Architecture

- 🌐 **Sunil-SSBots Custom TeraBox API Integration:**
  - Uses `https://sunil-ssbots.vercel.app/api/terabox?url={url}` for high-speed direct download links (DDL) and streaming URLs.
  - Supports all 20+ TeraBox mirrors (`teraboxlink.com`, `terabox.com`, `terabox.app`, `1024terabox.com`, etc.).
- 📺 **Interactive YouTube Video & Audio Downloader:**
  - Uses `https://sunil-ssbots.vercel.app/api/youtube?url={url}` to fetch candidate formats.
  - Informs the user to wait a few seconds while qualities are generated.
  - Displays inline quality selection buttons:
    - 🎬 **Video:** `1080p`, `720p`, `480p`, `360p`
    - 🎵 **Audio:** `MP3 (High Quality)`, `M4A (AAC)`
  - Downloads the selected quality and delivers it directly to Telegram!
- 🎬 **Diskwala Video Stream Resolver:**
  - Auto-resolves Diskwala share URLs into streamable video files.
- 🔐 **Dual-Channel Force Subscribe Verification:**
  - Enforces mandatory subscription to **Updates Channel** (`@SSBotsUpdates`) and **Loot Deals Channel** (`@Tg_Shoping`).
  - Interactive popup verification alert.
- 📦 **2GB Native MTProto Telegram Uploads:**
  - Real-time download & upload progress bars with speed in MB/s (`[▰▰▰▰▱▱▱▱] 45.2% ⚡ 22.4 MB/s`).
  - Native video streaming headers.

---

## 🛠️ Heroku Deployment Guide

### Option 1: 1-Click Heroku Deploy (GitHub)
1. Push this repository to your **GitHub** account.
2. Go to **[Heroku Dashboard](https://dashboard.heroku.com/)** > **New** > **Create new app**.
3. Under the **Deploy** tab, connect your GitHub repository and click **Deploy Branch**.
4. In **Settings** > **Config Vars**, fill in your credentials:
   - `API_ID`: Your Telegram API ID from [my.telegram.org](https://my.telegram.org)
   - `API_HASH`: Your Telegram API HASH from [my.telegram.org](https://my.telegram.org)
   - `BOT_TOKEN`: Your Telegram Bot Token from [@BotFather](https://t.me/BotFather)
   - `OWNER_USERNAME`: `Sunil_Sharma_2_0_Bot`
   - `UPDATES_CHANNEL`: `SSBotsUpdates`
   - `DEALS_CHANNEL`: `Tg_Shoping`
   - `MAX_FILE_SIZE_MB`: `2048`
5. In the **Resources** tab, activate the `worker` dyno (`worker: python3 bot.py`).

### Option 2: Heroku CLI
```bash
# Login to Heroku
heroku login

# Create App
heroku create terabox-diskwala-youtube-bot

# Set Config Vars
heroku config:set API_ID="1234567"
heroku config:set API_HASH="abcdef0123456789"
heroku config:set BOT_TOKEN="123456:ABC-DEF"
heroku config:set UPDATES_CHANNEL="SSBotsUpdates"
heroku config:set DEALS_CHANNEL="Tg_Shoping"
heroku config:set OWNER_USERNAME="Sunil_Sharma_2_0_Bot"
heroku config:set MAX_FILE_SIZE_MB="2048"

# Deploy
git push heroku main

# Start worker
heroku ps:scale worker=1

# Check live deployment logs
heroku logs --tail
```

---

## 📂 Repository File Map

```
├── bot.py             # Main Pyrogram MTProto Bot (TeraBox + Diskwala + YouTube + Dual F-Sub + 2GB Upload)
├── translations.py    # Stylish Typography, Inline Keyboards & YouTube Quality Buttons
├── resolvers.py       # Async Sunil-SSBots TeraBox, YouTube & Diskwala Resolvers
├── config.py          # Central Environment Configuration
├── requirements.txt   # Python Dependencies (pyrogram, tgcrypto, aiohttp, aiofiles)
├── Procfile           # Heroku Process File (worker: python3 bot.py)
├── runtime.txt        # Python 3.11 Runtime for Heroku
├── app.json           # Heroku 1-Click Deploy Manifest
├── .env.example       # Sample Environment Configuration
└── .gitignore         # Git Ignore Rules
```

---

<p align="center">
  <b>Developed with ❤️ by <a href="https://t.me/Sunil_Sharma_2_0_Bot">Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ</a></b><br>
  <i>Subscribe to <a href="https://www.youtube.com/@SunilWebTricks">SunilWebTricks on YouTube</a> for more awesome bots!</i>
</p>
