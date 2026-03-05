import gradio as gr
import os
import json
import tkinter as tk
from tkinter import filedialog
import re
from downloader import download_video

# Persistence file in project root
SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                saved_dir = data.get("download_dir")
                if saved_dir and os.path.isdir(saved_dir):
                    return saved_dir
        except Exception:
            pass
    default_dir = r"D:\Downloads\Video"
    os.makedirs(default_dir, exist_ok=True)
    return default_dir

def save_settings(download_dir: str):
    if download_dir:
        data = {"download_dir": download_dir}
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Warning: Could not save settings: {e}")

DEFAULT_DOWNLOAD_DIR = load_settings()

def browse_folder(current_dir: str):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    selected = filedialog.askdirectory(
        initialdir=current_dir or os.path.expanduser("~"),
        title="Select Download Folder"
    )
    root.destroy()
    if selected and os.path.isdir(selected):
        save_settings(selected)
        return selected
    return current_dir

def on_download(url: str, quality: str, highest_quality: bool, current_dir: str, progress=gr.Progress(track_tqdm=True)):
    """Main download handler with safe progress (fraction only) + status message"""
    def strip_ansi(text: str) -> str:
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def progress_hook(d):
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0%')
            clean_percent_str = strip_ansi(percent_str).strip()
            clean_number_match = re.search(r'[\d.]+', clean_percent_str)
            clean_number = clean_number_match.group(0) if clean_number_match else '0'
            try:
                frac = float(clean_number) / 100.0
                if not 0 <= frac <= 1:
                    frac = 0.0
            except (ValueError, TypeError):
                frac = 0.0
            desc = f"Downloading... {clean_number}%"
            progress(frac)  # Fraction only
            return desc
        elif d['status'] == 'finished':
            progress(1.0)
            return "Download finished, processing..."
        elif d['status'] == 'error':
            progress(0.0)
            return "Error during download"
        return ""

    path, message = download_video(
        url=url,
        output_dir=current_dir,
        quality=quality,
        highest_quality=highest_quality,
        progress_callback=progress_hook
    )

    final_status = message if message else "Download complete" if path else "Unknown status"

    if path:
        # Set value to the local filepath for browser download
        return final_status, gr.DownloadButton(value=path, label="Download File", visible=True)
    else:
        return final_status, gr.DownloadButton(visible=False)

# Custom CSS: Larger/balanced button text
custom_css = """
.gr-button {
    font-size: 1.15em !important;
    font-weight: 500 !important;
    padding: 0.75rem 1.25rem !important;
}
"""

with gr.Blocks(title="Widkapos") as demo:
    gr.Markdown("# Widkapos")

    download_dir_state = gr.State(value=DEFAULT_DOWNLOAD_DIR)
    highest_quality_state = gr.State(value=False)
    settings_visible = gr.State(value=False)

    with gr.Row(equal_height=True):
        url_input = gr.Textbox(
            label="Video URL",
            placeholder="https://www.youtube.com/watch?v=...",
            scale=4
        )
        download_btn = gr.Button(
            "Download",
            variant="primary",
            scale=1,
            min_width=140
        )

    with gr.Row(equal_height=True):
        quality_dropdown = gr.Dropdown(
            choices=["best", "1080p", "720p", "480p", "Audio only"],
            value="best",
            label="Video Quality",
            interactive=True,
            scale=4
        )
        gear_btn = gr.Button(
            "⚙️ Settings",
            variant="secondary",
            scale=1,
            min_width=140
        )

    settings_row = gr.Row(visible=False)
    with settings_row:
        highest_cb = gr.Checkbox(
            label="Download the highest quality video format available",
            value=False,
            info="Overrides quality dropdown → merges best video + audio"
        )

    with gr.Row(equal_height=True):
        download_location = gr.Textbox(
            value=DEFAULT_DOWNLOAD_DIR,
            label="Download Location",
            interactive=True,
            placeholder="Path to save videos...",
            scale=4
        )
        change_btn = gr.Button(
            "Change",
            variant="secondary",
            scale=1,
            min_width=140
        )

    status_output = gr.Textbox(label="Status", interactive=False, lines=3)
    download_output = gr.DownloadButton(label="Downloaded File (click to save)", visible=False, interactive=False)

    # Toggle settings visibility
    def toggle_settings(current_visible: bool):
        new_visible = not current_visible
        return new_visible, gr.update(visible=new_visible)

    gear_btn.click(
        fn=toggle_settings,
        inputs=settings_visible,
        outputs=[settings_visible, settings_row],
        show_progress="minimal"
    )

    highest_cb.change(
        fn=lambda val: val,
        inputs=highest_cb,
        outputs=highest_quality_state,
        show_progress="minimal"
    )

    change_btn.click(
        fn=browse_folder,
        inputs=download_dir_state,
        outputs=download_dir_state
    ).then(
        fn=lambda x: x,
        inputs=download_dir_state,
        outputs=download_location,
        show_progress="minimal"
    )

    download_btn.click(
        fn=on_download,
        inputs=[url_input, quality_dropdown, highest_quality_state, download_dir_state],
        outputs=[status_output, download_output]
    )

demo.queue().launch(
    allowed_paths=[
        os.path.expanduser("~"), 
        r"D:\Downloads\Video", 
        r"D:\Downloads\Music"          # ← add this line (or whatever path is in settings.json)
    ],
    theme=gr.themes.Default(text_size="lg"),
    css=custom_css
)