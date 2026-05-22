"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    YOUTUBE PLAYLIST & VIDEO DOWNLOADER                      ║
║                                                                            ║
║  Description : Downloads YouTube playlists and single videos in the        ║
║                highest quality available with automatic merging.            ║
║                                                                            ║
║  Powered by  : yt-dlp (https://github.com/yt-dlp/yt-dlp)                  ║
║                FFmpeg (https://ffmpeg.org)                                  ║
║                                                                            ║
║  GitHub      : https://github.com/akwasimm/Youtube-Video-Downloader-Script ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ══════════════════════════════════════════════════════════════════════════════

import sys
import os
import logging
from pathlib import Path
from datetime import datetime

from yt_dlp import YoutubeDL


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION — Edit these values to match your setup
# ══════════════════════════════════════════════════════════════════════════════

# Folder where all downloads will be saved
OUTPUT_FOLDER: str = r"D:\05_Yt Downloads"

# Full path to FFmpeg bin folder (run "where ffmpeg" in CMD to find this)
FFMPEG_FOLDER: str = (
    r"C:\Users\wasim\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1.1-full_build\bin"
)

# Your main playlist URL (used when you choose option 1 in the menu)
DEFAULT_PLAYLIST: str = (
    "https://youtube.com/playlist?list=PL1EghclDF616UbtVkSGH_yUdHI8gZLfC3&si=hXc5W4xsoqTWNsU3"
)


# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS — Do not change these unless you know what you're doing
# ══════════════════════════════════════════════════════════════════════════════

APP_NAME: str = "YouTube Downloader"
APP_VERSION: str = "2.0.0"
ARCHIVE_FILENAME: str = "downloaded_archive.txt"
LOG_FILENAME: str = "download_log.txt"
MERGE_FORMAT: str = "mkv"
LINE_WIDTH: int = 62


# ══════════════════════════════════════════════════════════════════════════════
# LOGGING SETUP — Suppress noisy yt-dlp and urllib3 warnings
# ══════════════════════════════════════════════════════════════════════════════

logging.getLogger("yt_dlp").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)


# ══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def clear_screen() -> None:
    """Clear the terminal screen for a clean look."""
    os.system("cls" if os.name == "nt" else "clear")


def format_size(size_bytes: float) -> str:
    """
    Convert bytes to a human-readable file size string.

    Args:
        size_bytes: File size in bytes.

    Returns:
        Formatted string like '125.4 MB' or '1.2 GB'.
    """
    if size_bytes is None or size_bytes <= 0:
        return "Unknown"

    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)

    for unit in units:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0

    return f"{size:.2f} PB"


def print_header() -> None:
    """Print the application header banner."""
    print()
    print(f"  ╔{'═' * (LINE_WIDTH - 4)}╗")
    print(f"  ║{'🎬 ' + APP_NAME + ' v' + APP_VERSION:^{LINE_WIDTH - 4}}║")
    print(f"  ╚{'═' * (LINE_WIDTH - 4)}╝")
    print()


def print_separator() -> None:
    """Print a visual separator line."""
    print(f"  {'─' * (LINE_WIDTH - 4)}")


def print_status(label: str, value: str) -> None:
    """
    Print a formatted status line.

    Args:
        label: The label text (e.g., 'Folder').
        value: The value text (e.g., 'D:\\Downloads').
    """
    print(f"  │ {label:<12} : {value}")


def is_playlist(url: str) -> bool:
    """
    Determine if a URL points to a YouTube playlist.

    Args:
        url: The YouTube URL to check.

    Returns:
        True if the URL contains playlist identifiers.
    """
    return "playlist?list=" in url or "&list=" in url


def log_download(output_path: Path, url: str, mode: str) -> None:
    """
    Append a download entry to the log file.

    Args:
        output_path: The base output directory.
        url: The downloaded URL.
        mode: Either 'PLAYLIST' or 'SINGLE'.
    """
    log_file = output_path / LOG_FILENAME
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{mode}] {url}\n")


# ══════════════════════════════════════════════════════════════════════════════
# DOWNLOAD TRACKING — Track files and sizes during download
# ══════════════════════════════════════════════════════════════════════════════

class DownloadTracker:
    """
    Tracks download progress, file counts, and total sizes
    across an entire download session.
    """

    def __init__(self) -> None:
        self.downloaded_count: int = 0
        self.skipped_count: int = 0
        self.error_count: int = 0
        self.total_bytes: float = 0
        self.current_video: str = ""

    def progress_hook(self, d: dict) -> None:
        """
        Hook function called by yt-dlp during download.

        Provides clean, formatted progress output without
        showing internal filenames or merge artifacts.

        Args:
            d: Dictionary containing download status information.
        """
        status = d.get("status", "")

        if status == "downloading":
            # ── Show clean progress bar ──────────────────────────────────
            percent = d.get("_percent_str", "  0.0%").strip()
            speed = d.get("_speed_str", "    ---").strip()
            eta = d.get("_eta_str", "  --:--").strip()
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)

            # Build a clean progress line
            size_info = ""
            if total and total > 0:
                size_info = f" │ Size: {format_size(total)}"

            progress_line = (
                f"\r  ⬇️  {percent} │ "
                f"Speed: {speed} │ "
                f"ETA: {eta}"
                f"{size_info}   "
            )
            print(progress_line, end="", flush=True)

        elif status == "finished":
            # ── Track completed file ─────────────────────────────────────
            file_size = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            if file_size:
                self.total_bytes += file_size

        elif status == "error":
            self.error_count += 1
            print(f"\n  ❌ Error occurred during download")

    def postprocessor_hook(self, d: dict) -> None:
        """
        Hook function called by yt-dlp during post-processing.

        Shows a clean message when merging is complete
        instead of showing raw FFmpeg merger output.

        Args:
            d: Dictionary containing post-processor status.
        """
        status = d.get("status", "")
        postprocessor = d.get("postprocessor", "")

        if status == "finished" and postprocessor == "Merger":
            # ── Extract clean filename from the info dict ────────────────
            info = d.get("info_dict", {})
            title = info.get("title", "Unknown")
            playlist_index = info.get("playlist_index", "")
            file_size_approx = info.get("filesize_approx", 0)

            # Try to get actual merged file size
            filepath = d.get("info_dict", {}).get("filepath", "")
            if filepath and Path(filepath).exists():
                actual_size = Path(filepath).stat().st_size
                size_str = format_size(actual_size)
            elif file_size_approx:
                size_str = format_size(file_size_approx)
            else:
                size_str = "Calculating..."

            # Clean display
            if playlist_index:
                display_name = f"{playlist_index:>3}. {title}"
            else:
                display_name = title

            self.downloaded_count += 1

            print(f"\n  ✅ {display_name}")
            print(f"     📦 Size: {size_str}")
            print_separator()


# ══════════════════════════════════════════════════════════════════════════════
# CORE DOWNLOAD FUNCTION
# ══════════════════════════════════════════════════════════════════════════════

def download(url: str) -> None:
    """
    Download a YouTube video or playlist.

    Automatically detects whether the URL is a playlist or single video,
    configures yt-dlp accordingly, and downloads in the highest quality
    with automatic merging.

    Args:
        url: YouTube video or playlist URL.
    """
    # ── Setup paths ──────────────────────────────────────────────────────
    output_path = Path(OUTPUT_FOLDER)
    output_path.mkdir(parents=True, exist_ok=True)

    archive_file = str(output_path / ARCHIVE_FILENAME)

    # ── Detect mode ──────────────────────────────────────────────────────
    playlist_mode = is_playlist(url)
    mode_label = "PLAYLIST" if playlist_mode else "SINGLE VIDEO"

    if playlist_mode:
        # Playlist: organized in subfolders with numbering
        outtmpl = str(
            output_path
            / "%(playlist_title)s"
            / "%(playlist_index)03d - %(title)s.%(ext)s"
        )
    else:
        # Single video: saved in 'Singles' subfolder
        outtmpl = str(
            output_path
            / "Singles"
            / "%(title)s.%(ext)s"
        )

    # ── Initialize download tracker ──────────────────────────────────────
    tracker = DownloadTracker()

    # ── yt-dlp configuration ─────────────────────────────────────────────
    ydl_opts = {
        # ── Quality: Best available video + audio ────────────────────────
        "format": "bestvideo+bestaudio/best",

        # ── Output template ──────────────────────────────────────────────
        "outtmpl": outtmpl,

        # ── FFmpeg: Required for merging video + audio ───────────────────
        "ffmpeg_location": FFMPEG_FOLDER,

        # ── Merge format: MKV for maximum codec compatibility ────────────
        "merge_output_format": MERGE_FORMAT,

        # ── Archive: Tracks downloaded videos to prevent duplicates ──────
        "download_archive": archive_file,

        # ── Playlist behavior ────────────────────────────────────────────
        "noplaylist": not playlist_mode,

        # ── Error handling: Continue on failures ─────────────────────────
        "ignoreerrors": True,
        "no_warnings": True,

        # ── Network reliability ──────────────────────────────────────────
        "continuedl": True,
        "retries": 15,
        "fragment_retries": 15,
        "concurrent_fragment_downloads": 4,
        "file_access_retries": 5,

        # ── Windows compatibility ────────────────────────────────────────
        "windowsfilenames": True,

        # ── Suppress all console output from yt-dlp itself ───────────────
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,

        # ── Hooks: Our clean custom output ───────────────────────────────
        "progress_hooks": [tracker.progress_hook],
        "postprocessor_hooks": [tracker.postprocessor_hook],
    }

    # ── Display download info ────────────────────────────────────────────
    print()
    print(f"  ┌{'─' * (LINE_WIDTH - 4)}┐")
    print(f"  │{'📋 ' + mode_label:^{LINE_WIDTH - 4}}│")
    print(f"  └{'─' * (LINE_WIDTH - 4)}┘")
    print()
    print_status("📁 Folder", str(output_path))
    print_status("🔗 URL", url[:50] + ("..." if len(url) > 50 else ""))
    print_status("🎞️  Quality", "Highest Available")
    print_status("📦 Format", f".{MERGE_FORMAT}")
    print_status("🕐 Started", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    print_separator()
    print()

    # ── Execute download ─────────────────────────────────────────────────
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # ── Log this session ─────────────────────────────────────────────────
    log_download(output_path, url, mode_label)

    # ── Print summary ────────────────────────────────────────────────────
    print()
    print(f"  ╔{'═' * (LINE_WIDTH - 4)}╗")
    print(f"  ║{'✅ DOWNLOAD COMPLETE':^{LINE_WIDTH - 4}}║")
    print(f"  ╠{'═' * (LINE_WIDTH - 4)}╣")
    print(f"  ║  📥 Downloaded : {tracker.downloaded_count:<{LINE_WIDTH - 23}}║")
    print(f"  ║  📦 Total Size : {format_size(tracker.total_bytes):<{LINE_WIDTH - 23}}║")

    if tracker.error_count > 0:
        print(f"  ║  ❌ Errors     : {tracker.error_count:<{LINE_WIDTH - 23}}║")

    print(f"  ║  📁 Saved in   : {str(output_path):<{LINE_WIDTH - 23}}║")
    print(f"  ║  🕐 Finished   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<{LINE_WIDTH - 23}}║")
    print(f"  ╚{'═' * (LINE_WIDTH - 4)}╝")
    print()


# ══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE MENU
# ══════════════════════════════════════════════════════════════════════════════

def show_menu() -> None:
    """
    Display an interactive menu for the user to choose
    between playlist download, single video, or exit.
    """
    while True:
        clear_screen()
        print_header()

        print("  ┌──────────────────────────────────────────────────────────┐")
        print("  │                                                          │")
        print("  │   [1]  📋  Download my playlist (new videos only)        │")
        print("  │   [2]  🎬  Download a single video                       │")
        print("  │   [3]  📂  Download a different playlist                 │")
        print("  │   [4]  🚪  Exit                                          │")
        print("  │                                                          │")
        print("  └──────────────────────────────────────────────────────────┘")
        print()

        choice = input("  👉 Choose an option [1/2/3/4]: ").strip()

        if choice == "1":
            # ── Download default playlist ────────────────────────────────
            if "YOUR_PLAYLIST_ID_HERE" in DEFAULT_PLAYLIST:
                print()
                print("  ⚠️  You haven't set your playlist URL yet!")
                print("     Open the script and edit DEFAULT_PLAYLIST.")
                print()
                input("  Press Enter to go back...")
            else:
                download(DEFAULT_PLAYLIST)
                input("  Press Enter to continue...")

        elif choice == "2":
            # ── Download single video ────────────────────────────────────
            print()
            url = input("  📎 Paste video URL: ").strip()

            if url:
                download(url)
            else:
                print("  ❌ No URL provided.")

            input("  Press Enter to continue...")

        elif choice == "3":
            # ── Download different playlist ──────────────────────────────
            print()
            url = input("  📎 Paste playlist URL: ").strip()

            if url:
                download(url)
            else:
                print("  ❌ No URL provided.")

            input("  Press Enter to continue...")

        elif choice == "4":
            # ── Exit application ─────────────────────────────────────────
            print()
            print("  👋 Goodbye!")
            print()
            sys.exit(0)

        else:
            print("  ❌ Invalid choice. Please try again.")
            input("  Press Enter to continue...")


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    """
    Entry point for the application.

    Usage:
        Interactive mode : python yt_downloader.py
        Direct download  : python yt_downloader.py "URL"

    Examples:
        python yt_downloader.py
        python yt_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
        python yt_downloader.py "https://www.youtube.com/playlist?list=PLAYLIST_ID"
    """

    if len(sys.argv) > 1:
        # ── Direct mode: URL passed as command line argument ─────────────
        download(sys.argv[1])
    else:
        # ── Interactive mode: Show menu ──────────────────────────────────
        show_menu()
