# ==============================================================================
# 🤖 Bot Developer / Owner : Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ
# 🌐 Developer URL        : https://t.me/Sunil_Sharma_2_0_Bot (@Sunil_Sharma_2_0_Bot)
# 📢 Telegram Channel     : https://t.me/SSBotsUpdates (@SSBotsUpdates)
# 📺 YouTube Channel      : https://www.youtube.com/@SunilWebTricks (SunilWebTricks)
# 💬 Ask Doubt / Contact   : @Sunil_Sharma_2_0_Bot
# ==============================================================================

import re
try:
    import aiohttp
except ImportError:
    aiohttp = None
import asyncio
import json
import urllib.request
from urllib.parse import urlparse, quote, parse_qs
import config

TERABOX_API_URL = getattr(config, "TERABOX_API_URL", "https://sunil-ssbots.vercel.app/api/terabox")
DISKWALA_API_URL = getattr(config, "DISKWALA_API_URL", "https://sunil-ssbots.vercel.app/api/diskwala")
YOUTUBE_API_URL = getattr(config, "YOUTUBE_API_URL", "https://sunil-ssbots.vercel.app/api/youtube")
YTULTRA_API_URL = getattr(config, "YTULTRA_API_URL", "https://api.ytultra.com/ikool/youtube/download")

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

# --- 2. YouTube Video & Audio API Resolver (ytultra.com Engine) ---
async def resolve_youtube(url: str):
    """
    Extracts high-speed video and audio streams from ytultra.com (https://www.ytultra.com/en/youtube-video-downloader/)
    Fetches all available video qualities (4K, 2K, 1080p, 720p, 480p, 360p, 240p, 144p) and the best audio stream
    for synchronized FFmpeg muxing.
    """
    m = re.search(r"(?:v=|\/|youtu\.be\/|embed\/|shorts\/)([a-zA-Z0-9_-]{11})", url)
    video_id = m.group(1) if m else ""
    standard_url = f"https://www.youtube.com/watch?v={video_id}" if video_id else url.strip()

    title = "YouTube Video"
    author = "YouTube Channel"
    thumbnail = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg" if video_id else ""

    headers = {
        "Content-Type": "application/json",
        "User-Agent": UA,
        "Origin": "https://www.ytultra.com",
        "Referer": "https://www.ytultra.com/en/youtube-video-downloader/",
        "Accept": "application/json"
    }

    # 1. Fetch title and author from oEmbed
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={quote(standard_url, safe='')}&format=json"
        if aiohttp:
            async with aiohttp.ClientSession(headers={"User-Agent": UA}) as s:
                async with s.get(oembed_url, timeout=aiohttp.ClientTimeout(total=8)) as oresp:
                    if oresp.status == 200:
                        oe_data = await oresp.json()
                        title = oe_data.get("title") or title
                        author = oe_data.get("author_name") or author
                        if not thumbnail:
                            thumbnail = oe_data.get("thumbnail_url") or thumbnail
        else:
            req_oe = urllib.request.Request(oembed_url, headers={"User-Agent": UA})
            loop = asyncio.get_event_loop()
            def fetch_oe():
                with urllib.request.urlopen(req_oe, timeout=5) as r:
                    return json.loads(r.read().decode("utf-8"))
            oe_data = await loop.run_in_executor(None, fetch_oe)
            title = oe_data.get("title") or title
            author = oe_data.get("author_name") or author
            if not thumbnail:
                thumbnail = oe_data.get("thumbnail_url") or thumbnail
    except Exception:
        pass

    # 2. Call ytultra API
    ytultra_endpoint = getattr(config, "YTULTRA_API_URL", "https://api.ytultra.com/ikool/youtube/download")
    payload = {"url": standard_url}

    data = None
    if aiohttp:
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(ytultra_endpoint, json=payload, timeout=aiohttp.ClientTimeout(total=25)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
        except Exception as e:
            print(f"[YTULTRA API ERROR] aiohttp failed: {e}")

    # Fallback to standard urllib if aiohttp encounters issues
    if not data:
        try:
            req = urllib.request.Request(
                ytultra_endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers
            )
            loop = asyncio.get_event_loop()
            def sync_fetch():
                with urllib.request.urlopen(req, timeout=20) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            data = await loop.run_in_executor(None, sync_fetch)
        except Exception as e:
            print(f"[YTULTRA API FALLBACK ERROR] urllib failed: {e}")

    if not data or (data.get("code") != "0000" and not data.get("data")):
        err_msg = data.get("msg") or data.get("error") if data else "ytultra.com did not respond."
        raise Exception(f"Failed to fetch streams from ytultra.com: {err_msg}")

    info = data.get("data") or {}
    if not thumbnail and info.get("imageUrl"):
        thumbnail = info.get("imageUrl")

    medias = info.get("medias") or []
    if not medias:
        raise Exception("No video or audio streams found on ytultra.com for this video.")

    # 3. Categorize into Video streams and Audio streams
    video_map = {}
    audio_streams = []

    for item in medias:
        url = item.get("url")
        if not url:
            continue
        fmt_str = str(item.get("format") or "").strip()
        fmt_lower = fmt_str.lower()
        file_size = item.get("fileSize")

        # Check if audio
        is_audio = any(ext in fmt_lower for ext in [".m4a", ".weba", ".mp3", ".aac"]) or ("audio" in fmt_lower and not any(v in fmt_lower for v in [".mp4", ".webm"]))
        if is_audio:
            audio_streams.append({
                "format": fmt_str,
                "url": url,
                "fileSize": file_size,
                "is_m4a": ".m4a" in fmt_lower
            })
        else:
            # Video stream
            q_tag = None
            label = None
            if "4k" in fmt_lower or "2160" in fmt_lower:
                q_tag = "4K"
                label = "🎬 4K (2160p)"
            elif "2k" in fmt_lower or "1440" in fmt_lower:
                q_tag = "2K"
                label = "🎬 2K (1440p)"
            elif "1080" in fmt_lower:
                q_tag = "1080p"
                label = "🎬 1080p MP4"
            elif "720" in fmt_lower:
                q_tag = "720p"
                label = "🎬 720p MP4"
            elif "480" in fmt_lower:
                q_tag = "480p"
                label = "🎬 480p MP4"
            elif "360" in fmt_lower:
                q_tag = "360p"
                label = "🎬 360p MP4"
            elif "240" in fmt_lower:
                q_tag = "240p"
                label = "🎬 240p MP4"
            elif "144" in fmt_lower:
                q_tag = "144p"
                label = "🎬 144p MP4"
            else:
                m_p = re.search(r"(\d{3,4}p)", fmt_str)
                if m_p:
                    q_tag = m_p.group(1)
                    label = f"🎬 {q_tag}"
                else:
                    q_tag = fmt_str.split()[0] if fmt_str else "video"
                    label = f"🎬 {q_tag}"

            ext = "webm" if ".webm" in fmt_lower else "mp4"

            # Prefer mp4 over webm for same resolution if available
            if q_tag not in video_map or (ext == "mp4" and video_map[q_tag]["ext"] == "webm"):
                video_map[q_tag] = {
                    "format": q_tag,
                    "label": label,
                    "raw_format": fmt_str,
                    "type": "video",
                    "ext": ext,
                    "size": format_size(file_size) if file_size else "Dynamic",
                    "size_bytes": file_size or 0,
                    "downloadUrl": url
                }

    # Pick the best audio stream (prefer m4a/aac, then largest size)
    best_audio = None
    m4a_audios = [a for a in audio_streams if a.get("is_m4a")]
    if m4a_audios:
        best_audio = m4a_audios[0]
    elif audio_streams:
        best_audio = max(audio_streams, key=lambda a: a.get("fileSize") or 0)

    best_audio_url = best_audio.get("url") if best_audio else None
    best_audio_size = best_audio.get("fileSize") if best_audio else 0

    # Build final download_links list in descending quality order
    quality_order = ["4K", "2K", "1080p", "720p", "480p", "360p", "240p", "144p"]
    download_links = []

    for q in quality_order:
        if q in video_map:
            v_item = video_map[q]
            v_item["audioUrl"] = best_audio_url
            download_links.append(v_item)

    for q, v_item in video_map.items():
        if q not in quality_order:
            v_item["audioUrl"] = best_audio_url
            download_links.append(v_item)

    # Append Audio options
    if best_audio_url:
        download_links.append({
            "format": "mp3",
            "label": "🎵 MP3 Audio (192k)",
            "type": "audio",
            "ext": "mp3",
            "size": format_size(best_audio_size) if best_audio_size else "Audio",
            "size_bytes": best_audio_size or 0,
            "downloadUrl": best_audio_url
        })
        download_links.append({
            "format": "m4a",
            "label": "🎵 M4A Audio (AAC)",
            "type": "audio",
            "ext": "m4a",
            "size": format_size(best_audio_size) if best_audio_size else "Audio",
            "size_bytes": best_audio_size or 0,
            "downloadUrl": best_audio_url
        })

    return {
        "provider": "YouTube (ytultra Engine)",
        "title": title,
        "author": author,
        "thumbnail": thumbnail,
        "download_links": download_links,
        "best_audio_url": best_audio_url,
        "video_id": video_id
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
