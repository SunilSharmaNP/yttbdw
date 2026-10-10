# ==============================================================================
# 🤖 Bot Developer / Owner : Ꞩᵾꞥīł Ꞩħⱥɍᵯⱥ ƻ.Ꝋ
# 🌐 Developer URL        : https://t.me/Sunil_Sharma_2_0_Bot (@Sunil_Sharma_2_0_Bot)
# 📢 Telegram Channel     : https://t.me/SSBotsUpdates (@SSBotsUpdates)
# 📺 YouTube Channel      : https://www.youtube.com/@SunilWebTricks (SunilWebTricks)
# 💬 Ask Doubt / Contact   : @Sunil_Sharma_2_0_Bot
# ==============================================================================

from __future__ import annotations

import re
import time
import hashlib
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

SAVENOW_API_KEY = "dfcb6d76f2f6a9894gjkege8a4ab232222"
SAVENOW_BASE = "https://p.savenow.to"

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

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

SAVENOW_HEADERS = {
    "User-Agent": UA,
    "Referer": "https://y2mate.yt/",
    "Origin": "https://y2mate.yt",
    "Accept": "application/json, text/plain, */*",
}

FORMAT_MAP = {
    "1080": {"id": "1080", "quality": "1080p", "label": "🎬 MP4 1080p FHD (Video + Audio)", "type": "video", "ext": "mp4", "bitrate": 4650000},
    "720":  {"id": "720",  "quality": "720p",  "label": "🎬 MP4 720p HD (Video + Audio)",   "type": "video", "ext": "mp4", "bitrate": 2950000},
    "480":  {"id": "480",  "quality": "480p",  "label": "🎬 MP4 480p SD (Video + Audio)",   "type": "video", "ext": "mp4", "bitrate": 1300000},
    "360":  {"id": "360",  "quality": "360p",  "label": "🎬 MP4 360p Low (Video + Audio)",  "type": "video", "ext": "mp4", "bitrate": 700000},
    "240":  {"id": "240",  "quality": "240p",  "label": "🎬 MP4 240p Low (Video + Audio)",  "type": "video", "ext": "mp4", "bitrate": 350000},
    "144":  {"id": "144",  "quality": "144p",  "label": "🎬 MP4 144p Low (Video + Audio)",  "type": "video", "ext": "mp4", "bitrate": 180000},
    "1440": {"id": "1440", "quality": "1440p", "label": "🎬 MP4 1440p 2K (Video + Audio)",  "type": "video", "ext": "mp4", "bitrate": 8000000},
    "4k":   {"id": "4k",   "quality": "4k",    "label": "🎬 WEBM 4K UHD (Video + Audio)",   "type": "video", "ext": "webm", "bitrate": 16000000},
    "mp3":  {"id": "mp3",  "quality": "320kbps", "label": "🎵 MP3 Audio (320kbps)",         "type": "audio", "ext": "mp3", "bitrate": 320000},
    "m4a":  {"id": "m4a",  "quality": "128kbps", "label": "🎵 M4A Audio (Original AAC)",    "type": "audio", "ext": "m4a", "bitrate": 128000},
}

DEFAULT_TARGET_FORMATS = ["1080", "720", "480", "360", "mp3", "m4a"]

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

# ─── 2. PoW Token Solver & Cache for Savenow / y2mate Engine ───
_cached_pow_token = None
_pow_token_expires_at = 0

async def _get_valid_pow_token(session: aiohttp.ClientSession) -> str:
    global _cached_pow_token, _pow_token_expires_at
    now = int(time.time())
    if _cached_pow_token and _pow_token_expires_at - 30 > now:
        return _cached_pow_token

    try:
        challenge_url = f"{SAVENOW_BASE}/api/pow/challenge"
        async with session.get(challenge_url, headers=SAVENOW_HEADERS, timeout=aiohttp.ClientTimeout(total=8)) as resp:
            if resp.status != 200:
                return None
            challenge_data = await resp.json()

        salt = challenge_data.get("salt")
        difficulty = int(challenge_data.get("difficulty") or 3)
        signature = challenge_data.get("signature")
        expires_at = challenge_data.get("expires_at")
        if not salt:
            return None

        prefix = "0" * difficulty
        nonce = 0
        start_t = time.time()
        solved_nonce = None

        while time.time() - start_t < 3.5:
            h = hashlib.sha256(f"{salt}:{nonce}".encode("utf-8")).hexdigest()
            if h.startswith(prefix):
                solved_nonce = nonce
                break
            nonce += 1

        if solved_nonce is None:
            return None

        verify_url = f"{SAVENOW_BASE}/api/pow/verify"
        payload = {
            "salt": salt,
            "difficulty": difficulty,
            "expires_at": expires_at,
            "signature": signature,
            "nonce": solved_nonce
        }
        async with session.post(verify_url, json=payload, headers=SAVENOW_HEADERS, timeout=aiohttp.ClientTimeout(total=8)) as v_resp:
            if v_resp.status != 200:
                return None
            body = await v_resp.json()
            if body.get("success") and body.get("token"):
                _cached_pow_token = body["token"]
                _pow_token_expires_at = int(body.get("expires_at") or (now + 300))
                return _cached_pow_token
    except Exception as e:
        print(f"[POW TOKEN WARNING] {e}")

    return None

async def _process_savenow_format(session: aiohttp.ClientSession, yt_url: str, fmt_id: str, token: str, quality_bytes: dict):
    headers = dict(SAVENOW_HEADERS)
    if token:
        headers["Authorization"] = f"Bearer {token}"

    api_url = (
        f"{SAVENOW_BASE}/api/v2/download"
        f"?format={quote(fmt_id)}"
        f"&url={quote(yt_url)}"
        f"&apikey={quote(SAVENOW_API_KEY)}"
    )

    fmt_info = FORMAT_MAP.get(fmt_id, {"id": fmt_id, "quality": f"{fmt_id}p", "label": fmt_id, "type": "video", "ext": "mp4"})

    try:
        async with session.get(api_url, headers=headers, timeout=aiohttp.ClientTimeout(total=18)) as resp:
            if resp.status not in (200, 201):
                return None
            data = await resp.json()

        dlink = data.get("download_url") or data.get("url")
        calc_bytes = quality_bytes.get(fmt_id) or 0
        size_str = format_size(calc_bytes) if calc_bytes else None

        if dlink:
            return {
                "format": fmt_id,
                "quality": fmt_info["quality"],
                "label": fmt_info["label"],
                "type": fmt_info["type"],
                "ext": fmt_info["ext"],
                "downloadUrl": dlink,
                "size": size_str or "Fast Stream",
                "size_bytes": calc_bytes
            }

        progress_url = data.get("progress_url")
        if not progress_url:
            return None

        # Poll until done (up to 30 tries, 1.5s interval)
        for _ in range(30):
            await asyncio.sleep(1.5)
            try:
                async with session.get(progress_url, headers=headers, timeout=aiohttp.ClientTimeout(total=8)) as p_resp:
                    if p_resp.status == 200:
                        p_data = await p_resp.json()
                        p_dlink = p_data.get("download_url") or p_data.get("url")
                        if p_dlink and len(p_dlink) > 5:
                            return {
                                "format": fmt_id,
                                "quality": fmt_info["quality"],
                                "label": fmt_info["label"],
                                "type": fmt_info["type"],
                                "ext": fmt_info["ext"],
                                "downloadUrl": p_dlink,
                                "size": size_str or "Fast Stream",
                                "size_bytes": calc_bytes
                            }
                        status = (p_data.get("text") or "").lower()
                        if status in ["error", "failed"]:
                            break
            except Exception:
                continue

    except Exception as e:
        print(f"[SAVENOW FORMAT ERROR] {fmt_id}: {e}")

    return None

# --- 2. YouTube Video & Audio API Resolver (y2mate.yt PoW & Savenow Engine) ---
async def resolve_youtube(url: str):
    """
    Upgraded with y2mate.yt Proof-of-Work (PoW) Engine & Savenow.to Multi-Server Network.
    Accurate Real YouTube Duration & File Size Calculation, Direct Chunked DDLs,
    and Clean Non-Duplicate Format Responses.
    """
    m = re.search(r"(?:v=|\/|youtu\.be\/|embed\/|shorts\/)([a-zA-Z0-9_-]{11})", url)
    video_id = m.group(1) if m else ""
    standard_url = f"https://www.youtube.com/watch?v={video_id}" if video_id else url.strip()

    title = "YouTube Video"
    author = "YouTube Channel"
    thumbnail = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg" if video_id else ""
    duration_seconds = 0
    quality_bytes = {}

    # Check if local Express API server is active on port 3000
    local_api = f"http://127.0.0.1:3000/api/youtube?url={quote(standard_url)}&all=true"
    async with aiohttp.ClientSession(headers={"User-Agent": UA}) as session:
        try:
            async with session.get(local_api, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status == 200:
                    api_json = await resp.json()
                    if api_json.get("success") and api_json.get("formats"):
                        download_links = []
                        for f in api_json["formats"]:
                            f_id = str(f.get("format") or "")
                            f_info = FORMAT_MAP.get(f_id, {"ext": "mp4", "type": "video"})
                            download_links.append({
                                "format": f_id,
                                "label": f.get("label") or f"{f_id}p",
                                "type": f_info["type"],
                                "ext": f_info["ext"],
                                "size": f.get("size") or "Fast DDL",
                                "size_bytes": f.get("bytes") or 0,
                                "downloadUrl": f.get("directUrl") or f.get("downloadUrl")
                            })

                        best_audio = next((l["downloadUrl"] for l in download_links if l["type"] == "audio"), None)
                        return {
                            "provider": "YouTube (y2mate.yt & Savenow PoW Engine)",
                            "title": api_json.get("title") or title,
                            "author": api_json.get("authorName") or author,
                            "thumbnail": api_json.get("thumbnailUrl") or thumbnail,
                            "download_links": download_links,
                            "best_audio_url": best_audio,
                            "video_id": video_id
                        }
        except Exception:
            pass

        # 1. Fetch title and author from oEmbed
        try:
            oembed_url = f"https://www.youtube.com/oembed?url={quote(standard_url, safe='')}&format=json"
            async with session.get(oembed_url, timeout=aiohttp.ClientTimeout(total=6)) as oresp:
                if oresp.status == 200:
                    oe_data = await oresp.json()
                    title = oe_data.get("title") or title
                    author = oe_data.get("author_name") or author
                    if not thumbnail:
                        thumbnail = oe_data.get("thumbnail_url") or thumbnail
        except Exception:
            pass

        # 2. Extract Real Duration via YouTube search query
        try:
            search_url = f"https://www.youtube.com/results?search_query={video_id}"
            async with session.get(search_url, timeout=aiohttp.ClientTimeout(total=6)) as sresp:
                if sresp.status == 200:
                    search_html = await sresp.text()
                    m_dur = re.search(r'"lengthText":[\s\S]{1,160}?"simpleText":\s*"(\d+:\d+(?::\d+)?)"', search_html)
                    if m_dur:
                        parts = [int(p) for p in m_dur.group(1).split(":")]
                        if len(parts) == 3:
                            duration_seconds = parts[0] * 3600 + parts[1] * 60 + parts[2]
                        elif len(parts) == 2:
                            duration_seconds = parts[0] * 60 + parts[1]
        except Exception:
            pass

        if duration_seconds > 0:
            for k, f_info in FORMAT_MAP.items():
                quality_bytes[k] = round((f_info["bitrate"] * duration_seconds) / 8)

        # 3. Solve PoW Token
        token = await _get_valid_pow_token(session)

        # 4. Process formats in parallel using Savenow Engine
        tasks = [
            _process_savenow_format(session, standard_url, fmt_id, token, quality_bytes)
            for fmt_id in DEFAULT_TARGET_FORMATS
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        download_links = []
        for r in results:
            if isinstance(r, dict) and r.get("downloadUrl"):
                download_links.append(r)

        if not download_links:
            # Direct proxy fallback link
            download_links.append({
                "format": "1080",
                "label": "🎬 MP4 1080p FHD (Video + Audio)",
                "type": "video",
                "ext": "mp4",
                "size": format_size(quality_bytes.get("1080")) if quality_bytes.get("1080") else "1080p MP4",
                "size_bytes": quality_bytes.get("1080", 0),
                "downloadUrl": f"http://127.0.0.1:3000/api/youtube?url={quote(standard_url)}&format=1080&dl=true"
            })
            download_links.append({
                "format": "720",
                "label": "🎬 MP4 720p HD (Video + Audio)",
                "type": "video",
                "ext": "mp4",
                "size": format_size(quality_bytes.get("720")) if quality_bytes.get("720") else "720p MP4",
                "size_bytes": quality_bytes.get("720", 0),
                "downloadUrl": f"http://127.0.0.1:3000/api/youtube?url={quote(standard_url)}&format=720&dl=true"
            })
            download_links.append({
                "format": "mp3",
                "label": "🎵 MP3 Audio (320kbps)",
                "type": "audio",
                "ext": "mp3",
                "size": format_size(quality_bytes.get("mp3")) if quality_bytes.get("mp3") else "320kbps MP3",
                "size_bytes": quality_bytes.get("mp3", 0),
                "downloadUrl": f"http://127.0.0.1:3000/api/youtube?url={quote(standard_url)}&format=mp3&dl=true"
            })

        best_audio = next((l["downloadUrl"] for l in download_links if l["type"] == "audio"), None)

        return {
            "provider": "YouTube (y2mate.yt & Savenow PoW Engine)",
            "title": title,
            "author": author,
            "thumbnail": thumbnail,
            "download_links": download_links,
            "best_audio_url": best_audio,
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
