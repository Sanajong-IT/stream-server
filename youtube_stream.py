import os
import subprocess
import time

def stream(video_path: str) -> None:
    """Stream a video file to YouTube in an endless loop."""
    stream_key = os.environ.get("YOUTUBE_STREAM_KEY")
    if not stream_key:
        raise RuntimeError("YOUTUBE_STREAM_KEY environment variable not set")

    youtube_rtmp = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"
    command = [
        "ffmpeg",
        "-re",  # read input at native frame rate
        "-stream_loop", "-1",  # loop video forever
        "-i", video_path,
        "-c", "copy",
        "-f", "flv",
        youtube_rtmp,
    ]

    while True:
        process = subprocess.Popen(command)
        process.wait()
        print("ffmpeg exited, restarting in 5 seconds...")
        time.sleep(5)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="24/7 YouTube streamer using FFmpeg")
    parser.add_argument("video", help="Path to the video file to loop")
    args = parser.parse_args()

    stream(args.video)
