# app/downloader.py
import os
from yt_dlp import YoutubeDL
from pathlib import Path
from config import TEMP_DIR

os.makedirs(TEMP_DIR, exist_ok=True)

def download_video(url: str, max_height:int):
    out_template = os.path.join(TEMP_DIR, "%(id)s.%(ext)s")
    if max_height and max_height>0:
        fmt = f"bestvideo[height<={max_height}]+bestaudio/best[height<={max_height}]"
    else:
        fmt = "bestvideo+bestaudio/best"
    ydl_opts = {
        "format": fmt,
        "outtmpl": out_template,
        "merge_output_format": "mp4",
        "nocheckcertificate": True,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        files = list(Path(TEMP_DIR).glob(f"{info['id']}*")) or []
        if not files:
            raise RuntimeError("Download failed or no files found")
        file = max(files, key=lambda p: p.stat().st_size)
        return str(file)

def download_audio(url: str):
    out_template = os.path.join(TEMP_DIR, "%(id)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "postprocessors": [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        "nocheckcertificate": True,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        files = list(Path(TEMP_DIR).glob(f"{info['id']}*")) or []
        if not files:
            raise RuntimeError("Audio download failed")
        file = max(files, key=lambda p: p.stat().st_size)
        return str(file)

def cleanup_file(path):
    try:
        os.remove(path)
    except Exception:
        pass
