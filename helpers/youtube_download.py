import asyncio
import os
import shutil
import sys
from urllib.parse import urlparse

from core.queue import TaskCancelledException, task_manager


YOUTUBE_STREAM_HOSTS = ("googlevideo.com",)
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/135.0.0.0 Safari/537.36"
)


def _validate_stream_url(stream_url: str) -> None:
    parsed = urlparse(stream_url or "")
    host = (parsed.hostname or "").lower()
    if (
        parsed.scheme != "https"
        or not any(host == domain or host.endswith(f".{domain}") for domain in YOUTUBE_STREAM_HOSTS)
    ):
        raise ValueError("Resolver did not return a valid HTTPS Google Video stream URL.")


async def download_youtube_stream(
    stream_url: str,
    output_path: str,
    progress_tracker,
    user_id: int,
) -> str:
    """Download the resolver's signed Google Video URL with yt-dlp; no YouTube cookies used."""
    _validate_stream_url(stream_url)

    output_dir = os.path.dirname(output_path) or "."
    os.makedirs(output_dir, exist_ok=True)
    temp_dir = f"{output_path}.yt-dlp-temp"
    os.makedirs(temp_dir, exist_ok=True)

    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--force-generic-extractor",
        "--no-playlist",
        "--no-warnings",
        "--newline",
        "--progress-template",
        "download:YT_PROGRESS %(progress.downloaded_bytes)s %(progress.total_bytes)s %(progress.total_bytes_estimate)s",
        "--add-headers",
        f"User-Agent:{USER_AGENT}",
        "--add-headers",
        "Referer:https://www.youtube.com/",
        "--add-headers",
        "Origin:https://www.youtube.com",
        "--output",
        output_path,
        "--paths",
        f"temp:{temp_dir}",
        stream_url,
    ]

    if user_id:
        task_manager.register_task_file(user_id, output_path)

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
                if len(values) >= 4:
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
        if return_code != 0:
            detail = " | ".join(error_lines[-3:])
            raise RuntimeError(
                "yt-dlp could not download the resolver stream"
                + (f": {detail[:800]}" if detail else f" (exit {return_code})")
            )
        if not os.path.isfile(output_path) or os.path.getsize(output_path) <= 1000:
            raise RuntimeError("yt-dlp finished without producing a valid media file.")
        return output_path
    finally:
        if proc is not None and proc.returncode is None:
            proc.kill()
            await proc.wait()
        shutil.rmtree(temp_dir, ignore_errors=True)
