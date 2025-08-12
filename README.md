# YouTube 24/7 Stream Server

This project contains a simple Python script that streams a video file to YouTube in a continuous loop. It uses [FFmpeg](https://ffmpeg.org/) to send the stream to YouTube's RTMP endpoint and automatically restarts the process if it exits.

## Requirements

- Python 3.8+
- FFmpeg installed and available in `PATH`
- A YouTube Live stream key

## Usage

1. Export your YouTube stream key so the script can use it:

   ```bash
   export YOUTUBE_STREAM_KEY=your_key_here
   ```

2. Run the streamer with the path to a video file you want to loop:

   ```bash
   python youtube_stream.py path/to/video.mp4
   ```

The script will loop the video endlessly and attempt to reconnect if the FFmpeg process exits.

## Docker

A lightweight Docker image can be built to run the streamer:

```bash
docker build -t youtube-streamer .
docker run --rm -e YOUTUBE_STREAM_KEY=your_key_here -v $(pwd)/video.mp4:/app/video.mp4 youtube-streamer /app/video.mp4
```

The container bundles FFmpeg and runs the streamer. Mount a video file into the container and specify its path when running.

## Note

Make sure you have the rights to broadcast the video content you are streaming to YouTube.
