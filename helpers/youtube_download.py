import asyncio
import os
import re
import shutil
import sys

from core.queue import TaskCancelledException, task_manager


def _max_height(quality: str) -> int:
    normalized = quality.lower()
    if "4k" in normalized:
        return 2160
    if "2k" in normalized:
        return 1440
    match = re.search(r"(\d{3,4})", normalized)
    if not match:
        raise ValueError(f"Unsupported YouTube quality: {quality}")
    return int(match.group(1))


async def download_youtube_video(
    video_id: str,
    quality: str,
    output_path: str,
    progress_tracker,
    user_id: int,
) -> str:
    """Download a fresh YouTube stream locally when an extracted link is rejected."""
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id or ""):
        raise ValueError("A valid YouTube video ID is required for the retry.")

    max_height = _max_height(quality)
    output_dir = os.path.dirname(output_path) or "."
    os.makedirs(output_dir, exist_ok=True)
    temp_dir = f"{output_path}.yt-dlp-temp"
    os.makedirs(temp_dir, exist_ok=True)

    format_selector = (
        f"bestvideo[height<={max_height}][ext=mp4]+bestaudio[ext=m4a]/"
        f"bestvideo[height<={max_height}]+bestaudio/"
        f"best[height<={max_height}][ext=mp4]/best[height<={max_height}]"
    )
    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--no-playlist",
        "--no-warnings",
        "--newline",
        "--progress-template",
        "download:YT_PROGRESS %(progress.downloaded_bytes)s %(progress.total_bytes)s %(progress.total_bytes_estimate)s",
        "--format",
        format_selector,
        "--merge-output-format",
        "mp4",
        "--output",
        output_path,
        "--paths",
        f"temp:{temp_dir}",
        f"https://www.youtube.com/watch?v={video_id}",
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
                "Fresh YouTube download failed"
                + (f": {detail[:800]}" if detail else f" (yt-dlp exit {return_code})")
            )
        if not os.path.isfile(output_path) or os.path.getsize(output_path) <= 1000:
            raise RuntimeError("yt-dlp finished without producing a valid video file.")
        return output_path
    finally:
        if proc is not None and proc.returncode is None:
            proc.kill()
            await proc.wait()
        shutil.rmtree(temp_dir, ignore_errors=True)
