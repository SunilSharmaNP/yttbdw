# ==============================================================================
# 🤖 Bot Developer / Owner : Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ
# 🌐 Developer URL        : https://t.me/Sunil_Sharma_2_0_Bot (@Sunil_Sharma_2_0_Bot)
# 📢 Telegram Channel     : https://t.me/SSBotsUpdates (@SSBotsUpdates)
# 📺 YouTube Channel      : https://www.youtube.com/@SunilWebTricks (SunilWebTricks)
# 💬 Ask Doubt / Contact   : @Sunil_Sharma_2_0_Bot
# ==============================================================================

import re
import aiohttp
from urllib.parse import urlparse, quote, parse_qs
import config

TERABOX_API_URL = getattr(config, "TERABOX_API_URL", "https://sunil-ssbots.vercel.app/api/terabox")
DISKWALA_API_URL = getattr(config, "DISKWALA_API_URL", "https://sunil-ssbots.vercel.app/api/diskwala")
YOUTUBE_API_URL = getattr(config, "YOUTUBE_API_URL", "https://sunil-ssbots.vercel.app/api/youtube")

TERABOX_HOSTS = {
    "terabox.com", "www.terabox.com", "terabox.app", "www.terabox.app",
    "teraboxapp.com", "www.teraboxapp.com", "1024terabox.com", "www.1024terabox.com",
    "1024tera.com", "www.1024tera.com", "1024tera.co", "teraboxlink.com", "freeterabox.com",
    "mirrobox.com", "momerybox.com", "tibibox.com", "nephobox.com", "4funbox.com", "dubox.com"
}

DISKWALA_HOSTS = {
    "diskwala.com", "www.diskwala.com", "diskwala.net", "www.diskwala.net",
    "diskwala.app", "www.diskwala.app", "thediskwala.com", "www.thediskwala.com"
}

YOUTUBE_HOSTS = {
    "youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com",
    "youtu.be", "www.youtu.be"
}

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

def format_size(bytes_num):
    n = float(bytes_num or 0)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if n < 1024.0:
            return f"{n:.2f} {unit}"
        n /= 1024.0
    return f"{n:.2f} PB"

def normalize_diskwala_url(input_url: str) -> str:
    """Normalizes any Diskwala URL into https://www.diskwala.com/app/<id>"""
    try:
        u = urlparse(input_url.strip())
        m = re.search(r'/(?:app|s|view|share|w|d)/([a-zA-Z0-9]+)', u.path)
        if m:
            return f"https://www.diskwala.com/app/{m.group(1)}"
        qs = parse_qs(u.query)
        if "id" in qs and qs["id"]:
            return f"https://www.diskwala.com/app/{qs['id'][0]}"
    except Exception:
        pass
    return input_url.strip()

def detect_link_type(url: str):
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname.lower() if parsed.hostname else ""
        if any(h in hostname for h in YOUTUBE_HOSTS):
            return "youtube"
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

# --- 1. TeraBox High-Speed API Resolver (sunil-ssbots engine) ---
async def resolve_terabox(url: str):
    headers = {"User-Agent": UA, "Accept": "application/json"}
    endpoint = f"{TERABOX_API_URL}?url={quote(url, safe='')}"
    
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(endpoint, timeout=aiohttp.ClientTimeout(total=45)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    
                    dlink = data.get("ddl") or data.get("download_url") or data.get("stream_url")
                    
                    details = data.get("details") or {}
                    items = data.get("items") or []
                    first_item = items[0] if items and isinstance(items, list) else {}
                    
                    name = details.get("name") or first_item.get("name") or first_item.get("file_name") or "terabox_media.mp4"
                    size = details.get("size") or first_item.get("size") or first_item.get("size_human") or "Unknown"
                    size_bytes = int(details.get("size_bytes") or first_item.get("size_bytes") or 0)
                    thumb = data.get("thumb_url") or data.get("thumbnailUrl") or first_item.get("thumb_url") or ""
                    
                    if not dlink and first_item:
                        dlink = first_item.get("ddl") or first_item.get("download_url") or first_item.get("stream_url")
                    
                    if not dlink and data.get("downloadLinks"):
                        dlink = data["downloadLinks"][-1].get("downloadUrl")
                    
                    if dlink:
                        return {
                            "provider": "TeraBox",
                            "name": name,
                            "size": size,
                            "size_bytes": size_bytes,
                            "dlink": dlink,
                            "thumbnail": thumb,
                            "stream_url": data.get("stream_url") or dlink
                        }
        except Exception as e:
            print(f"[TERABOX API NOTE] Primary API error: {e}")

        # Fallback to secondary mirror if main endpoint is busy
        backup_endpoints = [
            f"https://terabox-dl.qtcloud.workers.dev/api/get-info?url={quote(url, safe='')}",
            f"https://tera.backend.live/api/info?url={quote(url, safe='')}"
        ]
        for ep in backup_endpoints:
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

    raise Exception("TeraBox resolver could not extract download link. Please verify link is valid and public.")

# --- 2. YouTube Video & Audio API Resolver (sunil-ssbots engine) ---
async def resolve_youtube(url: str):
    headers = {"User-Agent": UA, "Accept": "application/json"}
    endpoint = f"{YOUTUBE_API_URL}?url={quote(url, safe='')}"
    
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(endpoint, timeout=aiohttp.ClientTimeout(total=90)) as resp:
            if resp.status != 200:
                raise Exception(f"YouTube API returned HTTP {resp.status}")
            data = await resp.json()
            if not data.get("success"):
                raise Exception(data.get("error") or "YouTube extraction failed.")
            
            title = data.get("title") or "YouTube Video"
            author = data.get("authorName") or "YouTube Channel"
            thumbnail = data.get("thumbnailUrl") or ""
            download_links = data.get("downloadLinks") or []
            
            if not download_links:
                raise Exception("No downloadable video or audio qualities found for this YouTube link.")
            
            return {
                "provider": "YouTube",
                "title": title,
                "author": author,
                "thumbnail": thumbnail,
                "download_links": download_links,
                "video_id": data.get("videoId") or ""
            }

# --- 3. Diskwala API Resolver (sunil-ssbots engine) ---
async def resolve_diskwala(url: str):
    headers = {"User-Agent": UA, "Accept": "application/json"}
    normalized_url = normalize_diskwala_url(url)
    endpoint = f"{DISKWALA_API_URL}?url={quote(normalized_url, safe='')}"
    
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(endpoint, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("success") and data.get("downloadUrl"):
                        title = (data.get("title") or "diskwala_video").strip()
                        if not title.lower().endswith(".mp4"):
                            title = f"{title}.mp4"
                        return {
                            "provider": "Diskwala",
                            "name": title,
                            "size": "Direct Stream",
                            "size_bytes": 0,
                            "dlink": data["downloadUrl"],
                            "thumbnail": ""
                        }
        except Exception as e:
            print(f"[DISKWALA API NOTE] Primary API error: {e}")

        # Fallback 1: thediskwala upstream resolver
        try:
            upstream_url = f"https://thediskwala.com/api/diskwala-free?url={quote(normalized_url, safe='')}"
            async with session.get(upstream_url, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("success") and data.get("url"):
                        title = (data.get("title") or "diskwala_video").strip()
                        if not title.lower().endswith(".mp4"):
                            title = f"{title}.mp4"
                        return {
                            "provider": "Diskwala",
                            "name": title,
                            "size": "Direct Stream",
                            "size_bytes": 0,
                            "dlink": data["url"],
                            "thumbnail": ""
                        }
        except Exception:
            pass

        # Fallback 2: Direct HTML Parser Fallback
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

    raise Exception("Diskwala link could not be resolved. Make sure the link is public and still accessible.")
