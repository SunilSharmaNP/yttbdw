# ==============================================================================
# 🤖 Bot Developer / Owner : Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ
# 🌐 Developer URL        : https://t.me/Sunil_Sharma_2_0_Bot (@Sunil_Sharma_2_0_Bot)
# 📢 Telegram Channel     : https://t.me/SSBotsUpdates (@SSBotsUpdates)
# 📺 YouTube Channel      : https://www.youtube.com/@SunilWebTricks (SunilWebTricks)
# 💬 Ask Doubt / Contact   : @Sunil_Sharma_2_0_Bot
# ==============================================================================

import re
import aiohttp
from urllib.parse import urlparse
import config

TERABOX_HOSTS = {
    "terabox.com", "www.terabox.com", "terabox.app", "www.terabox.app",
    "teraboxapp.com", "www.teraboxapp.com", "1024terabox.com", "www.1024terabox.com",
    "1024tera.com", "www.1024tera.com", "teraboxlink.com", "freeterabox.com",
    "mirrobox.com", "momerybox.com", "tibibox.com", "nephobox.com", "4funbox.com"
}

DISKWALA_HOSTS = {
    "diskwala.com", "www.diskwala.com", "diskwala.net", "www.diskwala.net",
    "diskwala.app", "www.diskwala.app"
}

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

def format_size(bytes_num):
    n = float(bytes_num or 0)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if n < 1024.0:
            return f"{n:.2f} {unit}"
        n /= 1024.0
    return f"{n:.2f} PB"

def detect_link_type(url: str):
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname.lower() if parsed.hostname else ""
        if any(h in hostname for h in TERABOX_HOSTS):
            return "terabox"
        if any(h in hostname for h in DISKWALA_HOSTS):
            return "diskwala"
    except Exception:
        pass
    return None

def extract_urls(text: str):
    pattern = r'https?://[^\s<>"\')\]]+'
    return re.findall(pattern, text or "")

# --- TeraBox Async Resolver ---
async def resolve_terabox(url: str):
    headers = {"User-Agent": UA, "Accept": "application/json"}
    
    proxy_endpoints = [
        f"https://terabox-dl.qtcloud.workers.dev/api/get-info?url={url}",
        f"https://tera.backend.live/api/info?url={url}"
    ]
    
    async with aiohttp.ClientSession(headers=headers) as session:
        for ep in proxy_endpoints:
            try:
                async with session.get(ep, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        files_list = data.get("list") or data.get("files") or (data.get("data") or {}).get("list")
                        if files_list and isinstance(files_list, list):
                            first = files_list[0]
                            file_name = first.get("server_filename") or first.get("filename") or first.get("name") or "terabox_file"
                            size_bytes = int(first.get("size") or 0)
                            dlink = first.get("dlink") or first.get("download_link") or first.get("direct_link")
                            thumb = first.get("thumbnail") or (first.get("thumbs") or {}).get("url3") or ""
                            
                            if dlink:
                                return {
                                    "provider": "TeraBox",
                                    "name": file_name,
                                    "size": format_size(size_bytes),
                                    "size_bytes": size_bytes,
                                    "dlink": dlink,
                                    "thumbnail": thumb
                                }
            except Exception:
                continue

    raise Exception("TeraBox resolver could not extract download URL. Verify link or active cookies.")

# --- Diskwala Async Resolver ---
async def resolve_diskwala(url: str):
    headers = {"User-Agent": UA, "Accept": "application/json"}
    api_url = f"{config.DISKWALA_RESOLVER_URL}?q={url}"
    
    async with aiohttp.ClientSession(headers=headers) as session:
        # 1. API Scraper
        try:
            async with session.get(api_url, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    file_info = (data.get("data") or {}).get("file") or data.get("file")
                    if data.get("success") and file_info and file_info.get("downloadUrl"):
                        ext = (file_info.get("extension") or "mp4").strip(".")
                        name = file_info.get("name") or "diskwala_video"
                        if not name.lower().endswith(f".{ext}"):
                            name = f"{name}.{ext}"
                        size_bytes = int(file_info.get("sizeBytes") or 0)
                        return {
                            "provider": "Diskwala",
                            "name": name,
                            "size": file_info.get("size") or format_size(size_bytes),
                            "size_bytes": size_bytes,
                            "dlink": file_info.get("downloadUrl"),
                            "thumbnail": file_info.get("thumbnail") or file_info.get("poster") or ""
                        }
        except Exception:
            pass

        # 2. Direct HTML Page Scrape Fallback
        try:
            async with session.get(url, headers={"User-Agent": UA, "Accept": "text/html"}, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    video_match = re.search(r'<video[^>]+src=["\']([^"\']+)["\']', html, re.I) or \
                                  re.search(r'<source[^>]+src=["\']([^"\']+)["\']', html, re.I) or \
                                  re.search(r'property=["\']og:video["\']\s+content=["\']([^"\']+)["\']', html, re.I)
                    if video_match:
                        dlink = video_match.group(1)
                        title_match = re.search(r'<title>([^<]+)</title>', html, re.I)
                        title = (title_match.group(1).split("-")[0].strip() if title_match else "diskwala_video") + ".mp4"
                        return {
                            "provider": "Diskwala",
                            "name": title,
                            "size": "Direct Stream",
                            "size_bytes": 0,
                            "dlink": dlink,
                            "thumbnail": ""
                        }
        except Exception:
            pass

    raise Exception("Diskwala link could not be resolved. Make sure the link is public.")
