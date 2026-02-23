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
    Downloads media with audio priority (for still-image videos) and MP3 output.
    Returns (filepath or None, status message)
    """
    if not url.strip():
        return None, "Error: Please enter a valid URL"

    if not os.path.isdir(output_dir):
        return None, "Error: Folder does not exist - " + output_dir

    ydl_opts = {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "quiet": False,
        "no_warnings": False,
        "progress_hooks": [progress_callback] if progress_callback else [],
        "cookiefile": "cookies.txt",
        # Enable remote components for better JS extraction (fixes skipped warning)
        "remote_components": ["ejs:github"],
        # Force audio-only extraction
        "format": "bestaudio/best",
        # Extract to MP3 (192 kbps)
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "format_sort": ["abr", "asr", "+size", "+acodec"],
    }

    if highest_quality or quality != "Audio only":
        ydl_opts["format"] = "bestaudio/best"  # Override to safe audio

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            if ydl_opts.get("postprocessors"):
                base, _ = os.path.splitext(filepath)
                filepath = base + ".mp3"
            title = info.get("title", "media")
            return filepath, "Success (audio only): Retrieved '" + title + "' to " + filepath
    except yt_dlp.utils.DownloadError as e:
        err_str = str(e)
        if "Requested format is not available" in err_str or "Only images" in err_str:
            return None, (
                "Video has no standard video stream (likely still image + audio).\n"
                "Audio extraction attempted - check folder for MP3 file.\n"
                "If nothing saved, re-export cookies.txt or use manual command."
            )
        elif "Sign in" in err_str or "bot" in err_str:
            return None, "Authentication failed. Re-export cookies.txt from logged-in browser."
        else:
            return None, "Download error: " + err_str
    except Exception as e:
        return None, "Unexpected error: " + str(e)