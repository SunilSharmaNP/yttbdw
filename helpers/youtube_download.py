import asyncio
import os
import shutil
import sys
from urllib.parse import urlparse
import aiohttp
import aiofiles

from core.queue import TaskCancelledException, task_manager


YOUTUBE_STREAM_HOSTS = ("googlevideo.com",)
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/135.0.0.0 Safari/537.36"
)


async def _download_direct_stream(
    stream_url: str,
    output_path: str,
    progress_tracker,
    user_id: int = 0
) -> bool:
    """Attempts direct HTTP streaming download of the Google Video media URL."""
    try:
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
            "Accept-Encoding": "identity;q=1, *;q=0",
            "Referer": "https://www.youtube.com/",
            "Origin": "https://www.youtube.com",
            "Connection": "keep-alive",
        }
        timeout = aiohttp.ClientTimeout(total=7200, connect=20)
        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
            async with session.get(stream_url, allow_redirects=True) as resp:
                if resp.status not in (200, 206):
                    print(f"[STREAM DOWNLOAD] HTTP {resp.status} for {stream_url[:120]}...")
                    return False
                total = int(resp.headers.get("content-length") or 0)
                received = 0
                async with aiofiles.open(output_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(2 * 1024 * 1024):
                        if user_id and task_manager.is_cancelled(user_id):
                            raise TaskCancelledException("Task cancelled by user.")
                        await f.write(chunk)
                        received += len(chunk)
                        if progress_tracker:
                            await progress_tracker.update(received, total)
        return os.path.isfile(output_path) and os.path.getsize(output_path) > 1000
    except (TaskCancelledException, asyncio.CancelledError):
        raise
    except Exception as e:
        print(f"[STREAM DOWNLOAD EXCEPTION] {e}")
        return False


async def _download_ffmpeg_stream(
    stream_url: str,
    output_path: str,
    user_id: int = 0
) -> bool:
    """Attempts stream copy via FFmpeg if direct HTTP stream has container quirks."""
    try:
        cmd = [
            "ffmpeg",
            "-y",
            "-headers",
            f"User-Agent: {USER_AGENT}\r\nReferer: https://www.youtube.com/\r\nOrigin: https://www.youtube.com\r\n",
            "-i",
            stream_url,
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            output_path,
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.wait()
        return os.path.isfile(output_path) and os.path.getsize(output_path) > 1000
    except Exception:
        return False


async def _download_with_ytdlp(
    youtube_url: str,
    output_path: str,
    progress_tracker,
    user_id: int = 0,
    quality_tag: str = None,
    is_audio: bool = False,
    status_msg = None
) -> str:
    """Downloads directly using yt-dlp with the original YouTube URL (WZML-X style)."""
    output_dir = os.path.dirname(output_path) or "."
    os.makedirs(output_dir, exist_ok=True)
    temp_dir = f"{output_path}.ytdlp-temp"
    os.makedirs(temp_dir, exist_ok=True)

    if is_audio:
        format_selector = "bestaudio[ext=m4a]/bestaudio/best"
    else:
        q = (quality_tag or "").lower()
        if "4k" in q or "2160" in q:
            format_selector = "bestvideo[height<=2160]+bestaudio/best[height<=2160]/best"
        elif "2k" in q or "1440" in q:
            format_selector = "bestvideo[height<=1440]+bestaudio/best[height<=1440]/best"
        elif "1080" in q:
            format_selector = "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
        elif "720" in q:
            format_selector = "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
        elif "480" in q:
            format_selector = "bestvideo[height<=480]+bestaudio/best[height<=480]/best"
        elif "360" in q:
            format_selector = "bestvideo[height<=360]+bestaudio/best[height<=360]/best"
        else:
            format_selector = "bestvideo+bestaudio/best"

    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--no-playlist",
        "--no-warnings",
        "--newline",
        "--progress-template",
        "download:YT_PROGRESS %(progress.downloaded_bytes)s %(progress.total_bytes)s %(progress.total_bytes_estimate)s",
        "--extractor-args",
        "youtube:player_client=android,web,tvhtml5",
        "-f",
        format_selector,
        "--output",
        output_path,
        "--paths",
        f"temp:{temp_dir}",
    ]
    if not is_audio:
        command.extend(["--merge-output-format", "mp4"])

    command.append(youtube_url)

    proc = None
    error_lines = []
    try:
        proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        while True:
            line = await proc.stdout.readline()
            if not line:
                break
            text = line.decode("utf-8", errors="replace").strip()
            if text.startswith("YT_PROGRESS "):
                values = text.split()
                if len(values) >= 4 and progress_tracker:
                    try:
                        current = int(values[1])
                        total = int(values[2]) if values[2].isdigit() else 0
                        if total <= 0 and values[3].isdigit():
                            total = int(values[3])
                        await progress_tracker.update(current, total)
                    except (ValueError, IndexError):
                        pass
            elif text:
                error_lines.append(text)
                error_lines = error_lines[-8:]

            if user_id and task_manager.is_cancelled(user_id):
                proc.terminate()
                await proc.wait()
                raise TaskCancelledException("Task cancelled by user.")

        return_code = await proc.wait()
        if return_code != 0 and not (os.path.isfile(output_path) and os.path.getsize(output_path) > 1000):
            detail = " | ".join(error_lines[-3:])
            raise RuntimeError(
                "yt-dlp could not download video"
                + (f": {detail[:600]}" if detail else f" (exit {return_code})")
            )

        # Verify output file (or .mp4 if yt-dlp appended extension)
        if os.path.isfile(output_path) and os.path.getsize(output_path) > 1000:
            return output_path
        if os.path.isfile(f"{output_path}.mp4") and os.path.getsize(f"{output_path}.mp4") > 1000:
            shutil.move(f"{output_path}.mp4", output_path)
            return output_path

        raise RuntimeError("yt-dlp finished without producing a valid media file.")
    finally:
        if proc is not None and proc.returncode is None:
            proc.kill()
            await proc.wait()
        shutil.rmtree(temp_dir, ignore_errors=True)


async def download_youtube_stream(
    stream_url: str,
    output_path: str,
    progress_tracker,
    user_id: int = 0,
    original_url: str = None,
    quality_tag: str = None,
    is_audio: bool = False,
    status_msg = None
) -> tuple[str, bool]:
    """
    Downloads YouTube video or audio.
    1. First attempts high-speed direct stream download (via aiohttp / ffmpeg).
    2. If stream URL is IP-bound (HTTP 403), expired, or fails, automatically falls back
       to direct yt-dlp downloading on the original YouTube URL (WZML-X engine style).
    Returns (downloaded_file_path, was_fallback).
    """
    if user_id:
        task_manager.register_task_file(user_id, output_path)

    output_dir = os.path.dirname(output_path) or "."
    os.makedirs(output_dir, exist_ok=True)

    # 1. Try Direct HTTP Stream Download if stream_url is provided
    if stream_url and stream_url.startswith("http"):
        print(f"[YOUTUBE DOWNLOAD] Attempting direct stream download for user {user_id}...")
        ok = await _download_direct_stream(stream_url, output_path, progress_tracker, user_id)
        if ok:
            return output_path, False

        # Try FFmpeg stream copy
        ok_ffmpeg = await _download_ffmpeg_stream(stream_url, output_path, user_id)
        if ok_ffmpeg:
            return output_path, False

    # 2. Fallback: Direct yt-dlp download using original YouTube URL (WZML-X style)
    if original_url:
        print(f"[YOUTUBE DOWNLOAD] Direct stream failed (e.g. 403 Forbidden IP restriction). Switching to yt-dlp on {original_url}...")
        if status_msg:
            try:
                await status_msg.edit_text(
                    "⚡ <b>Connecting via direct yt-dlp engine...</b>\n"
                    "<blockquote>🚀 <i>Bypassing stream IP lock & downloading at maximum speed...</i></blockquote>"
                )
            except Exception:
                pass

        result_path = await _download_with_ytdlp(
            youtube_url=original_url,
            output_path=output_path,
            progress_tracker=progress_tracker,
            user_id=user_id,
            quality_tag=quality_tag,
            is_audio=is_audio,
            status_msg=status_msg
        )
        return result_path, True

    raise RuntimeError("Direct resolver stream failed (HTTP 403/Forbidden) and no original YouTube URL was available for fallback.")
