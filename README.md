# 🎬 YouTube Playlist & Video Downloader

A simple Python script to download YouTube playlists and single videos
in the **highest quality available**, with automatic merging of video and audio.

> ⚠️ This project does not claim any ownership or credit.  
> All credit goes to the original creators of the tools used.  
> This is just a personal-use automation script.

---

## 📋 Table of Contents

- [What is this?](#what-is-this)
- [Features](#features)
- [Credits](#credits)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [How to Use](#how-to-use)
- [Folder Structure](#folder-structure)
- [FAQ](#faq)
- [Disclaimer](#disclaimer)

---

## 🤔 What is this?

This is a **Python automation script** that uses
[yt-dlp](https://github.com/yt-dlp/yt-dlp) and
[FFmpeg](https://ffmpeg.org/) to:

- Download an entire **YouTube playlist** in the highest quality available
- Download **single YouTube videos** in the highest quality available
- **Automatically merge** video and audio into a single `.mkv` file
- **Skip already downloaded** videos so you never download the same video twice
- Keep a **log file** of everything you have downloaded

It was built for personal use — specifically for downloading a single
personal YouTube playlist and keeping it updated with new videos over time.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎯 Highest quality | Downloads best video + best audio available |
| 🔀 Auto merge | Merges video and audio into `.mkv` using FFmpeg |
| ⏭️ Skip duplicates | Never re-downloads already downloaded videos |
| 📋 Playlist support | Downloads entire playlists with proper numbering |
| 🎬 Single video | Download individual videos directly |
| 📁 Organized folders | Saves inside named playlist folders automatically |
| 📄 Download log | Keeps a log of everything downloaded |
| 🖥️ Interactive menu | Simple menu to choose what to download |
| ⌨️ Command line | Supports direct URL as command line argument |
| 🪟 Windows safe | Sanitizes filenames for Windows compatibility |
| ♻️ Resume support | Resumes interrupted/partial downloads |

---

## 🙏 Credits

This project would not exist without these amazing open-source tools.
All credit goes to their respective creators and contributors:

---

### [yt-dlp](https://github.com/yt-dlp/yt-dlp)
> A feature-rich command-line audio/video downloader.  
> Fork of youtube-dl with additional features and fixes.  
> **License:** [The Unlicense](https://github.com/yt-dlp/yt-dlp/blob/master/LICENSE)  
> **GitHub:** https://github.com/yt-dlp/yt-dlp

---

### [FFmpeg](https://ffmpeg.org/)
> A complete, cross-platform solution to record, convert and stream audio and video.  
> Used in this project to merge separate video and audio streams into one file.  
> **License:** [LGPL / GPL](https://ffmpeg.org/legal.html)  
> **Website:** https://ffmpeg.org  
> **GitHub:** https://github.com/FFmpeg/FFmpeg

---

### [Gyan.dev FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/)
> Pre-built FFmpeg binaries for Windows.  
> Used for easy installation on Windows via WinGet.  
> **Website:** https://www.gyan.dev/ffmpeg/builds/

---

### [Python](https://www.python.org/)
> The programming language this script is written in.  
> **License:** [PSF License](https://docs.python.org/3/license.html)  
> **Website:** https://www.python.org

---

## 📦 Requirements

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.8 or higher | Run the script |
| yt-dlp | Latest | Download YouTube videos |
| FFmpeg | Any recent | Merge video and audio |

---

## 🛠️ Installation

Follow these steps carefully. Do them **in order**.

---

### Step 1 — Install Python

Download and install Python from the official website:

👉 https://www.python.org/downloads/

> ⚠️ **IMPORTANT:** During installation, make sure to check this box:
> ```
> ✅ Add Python to PATH
> ```

To verify Python is installed, open Command Prompt and run:

```bash
python --version
```

Expected output:

```
Python 3.x.x
```

---

### Step 2 — Install yt-dlp

Open Command Prompt and run:

```bash
pip install -U yt-dlp
```

To verify:

```bash
python -m yt_dlp --version
```

Expected output:

```
2026.xx.xx
```

---

### Step 3 — Install FFmpeg

Open Command Prompt and run:

```bash
winget install Gyan.FFmpeg
```

> ⚠️ After installation, **close and reopen** Command Prompt.

To verify:

```bash
ffmpeg -version
```

Expected output:

```
ffmpeg version x.x.x ...
```

---

### Step 4 — Find your FFmpeg path

Run this in Command Prompt:

```bash
where ffmpeg
```

You will see something like:

```
C:\Users\YourName\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe
```

Copy everything **except** `\ffmpeg.exe` at the end.
You will need this in the next step.

---

### Step 5 — Download the script

Download `yt_downloader.py` from this repository and save it anywhere.

Recommended location:

```
D:\05_Yt Downloads\yt_downloader.py
```

---

## ⚙️ Configuration

Open `yt_downloader.py` in any text editor (Notepad is fine).

Find this section at the top:

```python
# ===== CONFIGURATION =====
OUTPUT_FOLDER = r"D:\05_Yt Downloads"
FFMPEG_FOLDER = r"PASTE_YOUR_FFMPEG_PATH_HERE"
DEFAULT_PLAYLIST = "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID_HERE"
# =========================
```

Change these three values:

---

#### `OUTPUT_FOLDER`
The folder where all videos will be saved.

```python
OUTPUT_FOLDER = r"D:\05_Yt Downloads"
```

Change to whatever folder you want. For example:

```python
OUTPUT_FOLDER = r"C:\Users\YourName\Videos\YouTube"
```

---

#### `FFMPEG_FOLDER`
Paste the FFmpeg path you copied in Step 4 (without `\ffmpeg.exe`):

```python
FFMPEG_FOLDER = r"C:\Users\YourName\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin"
```

---

#### `DEFAULT_PLAYLIST`
Paste your YouTube playlist URL here:

```python
DEFAULT_PLAYLIST = "https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxxxxxxxx"
```

To get your playlist URL:
1. Open your playlist on YouTube
2. Copy the URL from the browser address bar
3. It should look like: `https://www.youtube.com/playlist?list=PLxxxx`

---

Save the file after making changes.

---

## 🚀 How to Use

### Method 1 — Interactive Menu

Open Command Prompt, navigate to where the script is saved, and run:

```bash
python yt_downloader.py
```

You will see this menu:

```
════════════════════════════════════════════════════════════
  🎬 YouTube Downloader
════════════════════════════════════════════════════════════

  1. Download my playlist (new videos only)
  2. Download a single video
  3. Download a different playlist
  4. Exit

  Choose [1/2/3/4]:
```

---

#### Option 1 — Download your playlist

Press `1` and hit Enter.

The script will:
- Connect to your configured playlist
- Skip any videos already downloaded
- Download only new videos
- Merge video and audio automatically

---

#### Option 2 — Download a single video

Press `2` and hit Enter.

Then paste any YouTube video URL:

```
https://www.youtube.com/watch?v=VIDEO_ID
```

The video will be saved in:

```
D:\05_Yt Downloads\Singles\Video Title.mkv
```

---

#### Option 3 — Download a different playlist

Press `3` and hit Enter.

Then paste any YouTube playlist URL:

```
https://www.youtube.com/playlist?list=PLAYLIST_ID
```

---

### Method 2 — Command Line (Direct URL)

You can also pass a URL directly without using the menu.

#### Download a single video:

```bash
python yt_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Download a playlist:

```bash
python yt_downloader.py "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

---

### Tip — Run from anywhere

If your script is saved at `D:\05_Yt Downloads\yt_downloader.py`,
you can run it from any folder like this:

```bash
python "D:\05_Yt Downloads\yt_downloader.py"
```

---

### Tip — Re-run to get new videos

Every time you add new videos to your playlist, just run the script again:

```bash
python yt_downloader.py
```

Press `1` for playlist.

It will **automatically skip** already downloaded videos
and only download the new ones. ✅

---

## 📁 Folder Structure

After downloading, your folder will look like this:

```
D:\
└── 05_Yt Downloads\
    │
    ├── My Playlist Name\
    │   ├── 001 - First Video Title.mkv
    │   ├── 002 - Second Video Title.mkv
    │   ├── 003 - Third Video Title.mkv
    │   └── ...
    │
    ├── Singles\
    │   ├── Some Video Title.mkv
    │   ├── Another Video Title.mkv
    │   └── ...
    │
    ├── downloaded_archive.txt   ← tracks downloaded videos (do not delete)
    └── download_log.txt         ← history of all download sessions
```

> ⚠️ **Do not delete `downloaded_archive.txt`**  
> This file is what prevents videos from being re-downloaded.  
> If you delete it, the script will re-download everything.

---

## ❓ FAQ

---

**Q: Why is the output file `.mkv` and not `.mp4`?**

MKV (Matroska) is a container format that supports any combination
of video and audio codecs without re-encoding.
This means **zero quality loss** during merging.
MP4 sometimes has compatibility issues with the highest quality streams.

---

**Q: Can I change the output format to MP4?**

Yes. Find this line in the script:

```python
"merge_output_format": "mkv",
```

Change it to:

```python
"merge_output_format": "mp4",
```

Note: Some very high quality streams may not merge cleanly into MP4.

---

**Q: A video was downloaded but not merged (separate video/audio files)?**

This means FFmpeg was not found during that download.
Make sure `FFMPEG_FOLDER` is set correctly in the configuration.
Then remove that video's entry from `downloaded_archive.txt` and run again.

---

**Q: Some videos in my playlist were skipped?**

Skipped videos are usually:
- Already downloaded (in archive)
- Deleted from YouTube
- Made private
- Age restricted
- Region blocked

The script uses `ignoreerrors: True` so it skips problem videos
and continues with the rest.

---

**Q: Can I use this for private playlists?**

No. This script only works with **public** YouTube playlists and videos.
Private video downloading would require browser cookie authentication
which is not included in this script.

---

**Q: Will this work on macOS or Linux?**

The script itself is cross-platform Python and will work on macOS and Linux.
However, the paths in the configuration section use Windows format.
You will need to change `OUTPUT_FOLDER` and `FFMPEG_FOLDER`
to use the correct format for your OS.

Linux / macOS example:

```python
OUTPUT_FOLDER = "/home/yourname/Videos/YouTube"
FFMPEG_FOLDER = "/usr/bin"
```

---

**Q: How do I update yt-dlp?**

YouTube changes frequently and yt-dlp needs to be kept updated.
Run this to update:

```bash
pip install -U yt-dlp
```

---

## ⚠️ Disclaimer

- This script is for **personal use only**.
- Only download videos that you have the **right to download**.
- Downloading copyrighted content without permission
  may violate YouTube's Terms of Service and copyright laws
  in your country.
- The author of this script takes **no responsibility**
  for how it is used.
- All tools used (yt-dlp, FFmpeg, Python) are independent
  open-source projects. This script is just a wrapper
  that uses them together.
- YouTube is a trademark of Google LLC.
  This project is not affiliated with or endorsed by Google or YouTube.

---

## 📄 License

This script itself has no license — it is released as-is for personal use.

All underlying tools have their own licenses:

| Tool | License |
|---|---|
| yt-dlp | [The Unlicense](https://github.com/yt-dlp/yt-dlp/blob/master/LICENSE) |
| FFmpeg | [LGPL / GPL](https://ffmpeg.org/legal.html) |
| Python | [PSF License](https://docs.python.org/3/license.html) |

---

*Made for personal use. No credit claimed.*
