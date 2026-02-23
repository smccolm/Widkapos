import yt_dlp
import os
from typing import Optional, Callable

def download_video(
    url: str,
    output_dir: str,
    quality: str = "best",
    highest_quality: bool = False,
    progress_callback: Optional[Callable] = None
) -> tuple[Optional[str], str]:
    """
    Downloads video using yt-dlp.
    Returns (filepath or None, status message)
    """
    if not url.strip():
        return None, "Error: Please enter a valid URL"

    if not os.path.isdir(output_dir):
        return None, f"Error: Download folder does not exist - {output_dir}"

    ydl_opts = {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "quiet": False,
        "no_warnings": False,
        "progress_hooks": [progress_callback] if progress_callback else [],
    }

    if highest_quality:
        ydl_opts["format"] = "bestvideo+bestaudio/best"
    else:
        # Simple quality mapping - extend later
        format_map = {
            "720p": "bestvideo[height<=720]+bestaudio/best",
            "1080p": "bestvideo[height<=1080]+bestaudio/best",
            "480p": "bestvideo[height<=480]+bestaudio/best",
            "Audio only": "bestaudio/best",
        }
        ydl_opts["format"] = format_map.get(quality, "bestvideo+bestaudio/best")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            title = info.get("title", "video")
            return filepath, f"Success: Downloaded '{title}' to {filepath}"
    except Exception as e:
        return None, f"Error: {str(e)}"