import os
import shutil
from helpers.aria2 import download_with_aria2c
from core.queue import task_manager

async def download_youtube_stream(
    stream_url: str,
    output_path: str,
    progress_tracker=None,
    user_id: int = 0,
    original_url: str = None,
    quality_tag: str = None,
    is_audio: bool = False,
    status_msg = None
) -> tuple[str, bool]:
    """
    Downloads YouTube media using aria2c high-speed multi-threaded engine.
    Connects with up to 16 parallel chunks directly to the Savenow / y2mate PoW DDL stream.
    Returns (output_path, was_fallback).
    """
    if user_id:
        task_manager.register_task_file(user_id, output_path)

    output_dir = os.path.dirname(output_path) or "."
    os.makedirs(output_dir, exist_ok=True)

    if not stream_url or not stream_url.startswith("http"):
        raise ValueError("Invalid YouTube DDL stream URL provided.")

    print(f"[YOUTUBE ARIA2C] Starting 16-connection download for user {user_id}: {output_path}")
    downloaded_file = await download_with_aria2c(
        url=stream_url,
        output_path=output_path,
        progress_tracker=progress_tracker,
        user_id=user_id,
        connections=16,
        referer="https://y2mate.yt/"
    )

    return downloaded_file, False
