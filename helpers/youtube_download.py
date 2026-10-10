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

    if "127.0.0.1" in stream_url or "localhost" in stream_url:
        print(f"[YOUTUBE SSEngine] Intercepted localhost stream URL, resolving direct CDN URL for {quality_tag}...")
        from resolvers import get_youtube_stream_url
        resolved = await get_youtube_stream_url(original_url or "", quality_tag or ("mp3" if is_audio else "720"))
        if resolved and resolved.startswith("http") and "127.0.0.1" not in resolved and "localhost" not in resolved:
            stream_url = resolved
        else:
            raise ValueError("Could not resolve external CDN stream URL for YouTube video.")

    print(f"[YOUTUBE SSENGINE] Starting 16-connection download for user {user_id}: {output_path}")
    downloaded_file = await download_with_aria2c(
        url=stream_url,
        output_path=output_path,
        progress_tracker=progress_tracker,
        user_id=user_id,
        connections=16,
        referer=""
    )

    return downloaded_file, False
