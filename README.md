# 🧬 Widkapos – Intelligent Media Acquisition Tool

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Gradio 6.x](https://img.shields.io/badge/Gradio-6.x-orange)](https://www.gradio.app/)
[![yt-dlp](https://img.shields.io/badge/Backend-yt--dlp-green)](https://github.com/yt-dlp/yt-dlp)
[![Windows 11](https://img.shields.io/badge/OS-Windows%2011-blue?logo=windows)](https://www.microsoft.com/windows)

A clean, modern, AI-assisted desktop application for intelligent media retrieval.

Built with **Gradio** for an elegant interface and **yt-dlp** for robust stream processing logic.

![Application Interface](./assets/screenshot.png)

------------------------------------------------------------------------

## 🤖 AI Agent & Developer Summary

- **Frontend:** Gradio 6.x – responsive, modern Blocks interface
- **Backend:** yt-dlp (latest stable) – powerful format selection & merging
- **Key UX Features:**
  - Native Windows folder picker (tkinter)
  - Persistent storage location (settings.json)
  - Toggleable high-fidelity mode
  - Real-time progress visualization & status feedback
  - Clean error handling & success retrieval button
- **Hardware Target:** Any modern Windows 11 machine (CPU-only or GPU optional)
- **Environment:** Python 3.13 + venv isolation

------------------------------------------------------------------------

## 🚀 Why Widkapos?

Modern media often arrives in fragmented formats. Widkapos provides:

- Simple, beautiful interface (no command line required)
- One-click format selection + highest-fidelity override
- Persistent storage choice across sessions
- Reliable combination of best video + audio streams
- Progress visualization that actually works

All in a lightweight, local-first desktop application.

------------------------------------------------------------------------

## 🛠️ Installation (Windows 11)

### 1. Prerequisites

- Python 3.13 (recommended: from python.org installer)
- Git (optional, for cloning)
- FFmpeg in system PATH (required for stream merging)

### 2. One-Time Setup

```cmd
cd E:\Widkapos
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

![Application Interface](./assets/Widkapos.png)