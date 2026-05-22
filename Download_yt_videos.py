from pathlib import Path
from yt_dlp import YoutubeDL
from datetime import datetime
import sys

# ===== CONFIGURATION =====
# Add download folder and FFmpeg path here
# Example: 
OUTPUT_FOLDER = r"D:\05_Yt Downloads"
# FFMPEG_FOLDER = r"C:\path\to\ffmpeg\bin" use where you have FFmpeg installed
FFMPEG_FOLDER = " "

# Your main playlist URL (used when no URL is provided)
DEFAULT_PLAYLIST = "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID_HERE"
# =========================


def progress_hook(d):
    if d["status"] == "finished":
        print(f"\n✅ Finished: {Path(d['filename']).name}")
    elif d["status"] == "downloading":
        percent = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        print(f"\r⬇️  {percent} | Speed: {speed} | ETA: {eta}    ", end="", flush=True)


def is_playlist(url):
    """Check if URL is a playlist."""
    return "playlist?list=" in url or "&list=" in url


def download(url):
    output_path = Path(OUTPUT_FOLDER)
    output_path.mkdir(parents=True, exist_ok=True)

    # Detect if playlist or single video
    playlist_mode = is_playlist(url)

    if playlist_mode:
        # Playlist: save inside playlist folder with numbering
        outtmpl = str(output_path / "%(playlist_title)s" / "%(playlist_index)03d - %(title)s.%(ext)s")
        archive_file = str(output_path / "downloaded_archive.txt")
        print("\n📋 Mode: PLAYLIST")
    else:
        # Single video: save directly in output folder
        outtmpl = str(output_path / "Singles" / "%(title)s.%(ext)s")
        archive_file = str(output_path / "downloaded_archive.txt")
        print("\n🎬 Mode: SINGLE VIDEO")

    ydl_opts = {
        # Highest quality
        "format": "bestvideo+bestaudio/best",

        # Output path
        "outtmpl": outtmpl,

        # FFmpeg for merging
        "ffmpeg_location": FFMPEG_FOLDER,

        # Merge into MKV
        "merge_output_format": "mkv",

        # Skip already downloaded
        "download_archive": archive_file,

        # Reliability
        "ignoreerrors": True,
        "continuedl": True,
        "retries": 10,
        "fragment_retries": 10,
        "concurrent_fragment_downloads": 4,

        # Windows-safe filenames
        "windowsfilenames": True,

        # For single video, don't download entire playlist if URL has &list=
        "noplaylist": not playlist_mode,

        # Progress
        "progress_hooks": [progress_hook],
    }

    print("═" * 60)
    print(f"  📁 Folder  : {output_path}")
    print(f"  🔗 URL     : {url[:60]}...")
    print(f"  🕐 Time    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("═" * 60)
    print()

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Log download
    log_file = output_path / "download_log.txt"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {url}\n")

    print()
    print("═" * 60)
    print("  ✅ DONE!")
    print(f"  📁 Saved in: {output_path}")
    print("═" * 60)
    print()


def show_menu():
    print()
    print("═" * 60)
    print("  🎬 YouTube Downloader")
    print("═" * 60)
    print()
    print("  1. Download my playlist (new videos only)")
    print("  2. Download a single video")
    print("  3. Download a different playlist")
    print("  4. Exit")
    print()

    choice = input("  Choose [1/2/3/4]: ").strip()

    if choice == "1":
        download(DEFAULT_PLAYLIST)
    elif choice == "2":
        url = input("  Paste video URL: ").strip()
        if url:
            download(url)
        else:
            print("  ❌ No URL provided.")
    elif choice == "3":
        url = input("  Paste playlist URL: ").strip()
        if url:
            download(url)
        else:
            print("  ❌ No URL provided.")
    elif choice == "4":
        print("  Bye!")
        sys.exit(0)
    else:
        print("  ❌ Invalid choice.")

    # Ask again
    input("\n  Press Enter to continue...")
    show_menu()


if __name__ == "__main__":
    # If URL provided as command line argument
    if len(sys.argv) > 1:
        url = sys.argv[1]
        download(url)
    else:
        # Show interactive menu
        show_menu()