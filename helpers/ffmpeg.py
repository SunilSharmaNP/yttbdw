import os
import re
import json
import time
import asyncio
import config

DOWNLOAD_DIR = getattr(config, "DOWNLOAD_DIR", "./downloads")

async def mux_media_ffmpeg(video_path: str, audio_path: str, output_path: str) -> bool:
    """
    Ultra-fast muxing of video stream and audio stream using FFmpeg.
    Uses stream copy (-c copy) when codecs permit (0% CPU re-encoding, takes < 1 second).
    Falls back to AAC audio encode if container requires conversion.
    """
    try:
        # 1. First attempt: Stream Copy (Instantaneous, Lossless)
        cmd_copy = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c", "copy",
            "-map", "0:v:0",
            "-map", "1:a:0?",
            "-shortest",
            output_path
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd_copy,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.communicate()
        if proc.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            return True

        # 2. Second attempt: Video copy with AAC audio encoder
        cmd_aac = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0?",
            "-shortest",
            output_path
        ]
        proc2 = await asyncio.create_subprocess_exec(
            *cmd_aac,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc2.communicate()
        if proc2.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            return True
    except Exception as e:
        print(f"[FFMPEG MUX ERROR] {e}")

    return False

async def convert_to_mp3_ffmpeg(audio_path: str, output_path: str) -> bool:
    """Converts downloaded audio stream to standard 192k MP3 using FFmpeg."""
    try:
        cmd = [
            "ffmpeg", "-y",
            "-i", audio_path,
            "-vn",
            "-acodec", "libmp3lame",
            "-b:a", "192k",
            output_path
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.communicate()
        if proc.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            return True
    except Exception as e:
        print(f"[FFMPEG MP3 ERROR] {e}")
    return False

async def get_video_metadata(video_path: str) -> dict:
    """
    Extracts video duration (in seconds), width, height, and thumbnail using ffprobe/ffmpeg.
    Fixes the TeraBox '00:00' duration bug by inspecting container format & stream headers.
    Also extracts a clean snapshot thumbnail from the video for the Telegram video player!
    """
    duration = 0
    width = 1280
    height = 720
    thumb_path = None

    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,duration",
            "-show_entries", "format=duration",
            "-of", "json",
            video_path
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        if proc.returncode == 0 and stdout:
            data = json.loads(stdout.decode())
            dur_str = data.get("format", {}).get("duration")
            if not dur_str and data.get("streams"):
                dur_str = data["streams"][0].get("duration")
            if dur_str:
                duration = int(float(dur_str))

            if data.get("streams") and len(data["streams"]) > 0:
                s0 = data["streams"][0]
                width = int(s0.get("width") or 1280)
                height = int(s0.get("height") or 720)
    except Exception as e:
        print(f"[FFPROBE METADATA ERROR] {e}")

    # Fallback 1: ffmpeg -i parsing if ffprobe returned 0 duration
    if duration == 0:
        try:
            cmd_info = ["ffmpeg", "-i", video_path]
            proc_info = await asyncio.create_subprocess_exec(
                *cmd_info,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            _, stderr = await proc_info.communicate()
            match_dur = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", stderr.decode("utf-8", errors="ignore"))
            if match_dur:
                hours = int(match_dur.group(1))
                minutes = int(match_dur.group(2))
                seconds = float(match_dur.group(3))
                duration = int(hours * 3600 + minutes * 60 + seconds)
        except Exception as e:
            print(f"[FFMPEG DURATION PARSE ERROR] {e}")

    # Fallback 2: Faststart remux for TeraBox videos (fixes moov atom & 00:00 duration)
    if duration == 0 and os.path.exists(video_path):
        try:
            faststart_temp = video_path + ".faststart.mp4"
            cmd_fast = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-c", "copy",
                "-movflags", "+faststart",
                faststart_temp
            ]
            proc_f = await asyncio.create_subprocess_exec(
                *cmd_fast,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc_f.communicate()
            if proc_f.returncode == 0 and os.path.exists(faststart_temp) and os.path.getsize(faststart_temp) > 1000:
                os.replace(faststart_temp, video_path)
                cmd_recheck = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", video_path]
                proc_r = await asyncio.create_subprocess_exec(
                    *cmd_recheck,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                sout, _ = await proc_r.communicate()
                if sout:
                    d_obj = json.loads(sout.decode())
                    d_str = d_obj.get("format", {}).get("duration")
                    if d_str:
                        duration = int(float(d_str))
        except Exception as e:
            print(f"[FASTSTART DURATION FIX NOTE] {e}")

    # Generate a thumbnail frame with ffmpeg
    try:
        ts = int(time.time())
        t_path = os.path.join(DOWNLOAD_DIR, f"{ts}_thumb.jpg")
        seek_sec = "00:00:02" if duration > 3 else "00:00:00.5"
        cmd_thumb = [
            "ffmpeg", "-y",
            "-ss", seek_sec,
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            t_path
        ]
        proc_t = await asyncio.create_subprocess_exec(
            *cmd_thumb,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc_t.communicate()
        if proc_t.returncode == 0 and os.path.exists(t_path) and os.path.getsize(t_path) > 100:
            thumb_path = t_path
    except Exception as e:
        print(f"[THUMBNAIL EXTRACTION ERROR] {e}")

    return {
        "duration": duration,
        "width": width,
        "height": height,
        "thumb": thumb_path
    }
