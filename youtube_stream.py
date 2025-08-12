import itertools
import os
import subprocess
import time
from pathlib import Path
from typing import Iterator

VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".flv", ".avi"}


def _iter_videos(path: str) -> Iterator[Path]:
    """Return an endless iterator of video files from *path*."""
    target = Path(path)
    if target.is_file():
        return itertools.cycle([target])
    if target.is_dir():
        files = sorted(
            f for f in target.iterdir() if f.is_file() and f.suffix.lower() in VIDEO_EXTENSIONS
        )
        if not files:
            raise RuntimeError(f"No video files found in directory {path}")
        return itertools.cycle(files)
    raise RuntimeError(f"{path} is not a valid file or directory")


def stream(video_path: str) -> None:
    """Stream video files to YouTube in an endless loop."""
    stream_key = os.environ.get("YOUTUBE_STREAM_KEY")
    if not stream_key:
        raise RuntimeError("YOUTUBE_STREAM_KEY environment variable not set")

    youtube_rtmp = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

    for video in _iter_videos(video_path):
        command = [
            "ffmpeg",
            "-re",  # read input at native frame rate
            "-i", str(video),
            "-c", "copy",
            "-f", "flv",
            youtube_rtmp,
        ]

        process = subprocess.Popen(command)
        process.wait()
        print(f"ffmpeg exited after streaming {video}, restarting in 5 seconds...")
        time.sleep(5)



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="24/7 YouTube streamer using FFmpeg")
    parser.add_argument(
        "video",
        nargs="?",
        help=(
            "Path to a video file or directory of video files to loop. "
            "If omitted, the path is read from the VIDEO_PATH environment variable."
        ),
    )
    args = parser.parse_args()

    video_path = args.video or os.environ.get("VIDEO_PATH")
    if not video_path:
        parser.error("Please provide a video path or set the VIDEO_PATH environment variable")

    stream(video_path)
