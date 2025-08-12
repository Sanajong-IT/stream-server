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

2. Run the streamer with the path to a video file **or** a directory containing
   multiple video files:

   ```bash
   # Single file
   python youtube_stream.py path/to/video.mp4

   # Directory of files (played in order)
   python youtube_stream.py /path/to/videos

   # Or set the path via an environment variable
   export VIDEO_PATH=/path/to/videos
   python youtube_stream.py
   ```

The script will stream each file once and continue looping through the list
forever, restarting FFmpeg if it exits.

## Docker

A lightweight Docker image can be built to run the streamer:

```bash
docker build -t youtube-streamer .
docker run --rm -e YOUTUBE_STREAM_KEY=your_key_here -e VIDEO_PATH=/app/video.mp4 -v $(pwd)/video.mp4:/app/video.mp4 youtube-streamer

# Or mount a directory of videos
docker run --rm -e YOUTUBE_STREAM_KEY=your_key_here -e VIDEO_PATH=/app/videos -v $(pwd)/videos:/app/videos youtube-streamer
```

The container bundles FFmpeg and runs the streamer. Mount a video file or
directory into the container and set the `VIDEO_PATH` environment variable to
the mounted location.

## Docker Compose

1. Copy `.env.template` to `.env` and fill in your stream key. Adjust
   `VIDEO_PATH` if you want the files mounted somewhere else in the
   container.
2. Ensure a `videos/` directory exists alongside the compose file and
   contains the files you want to loop.
3. Start the streamer:

   ```bash
   docker-compose up -d
   ```

The compose file builds the image, mounts the `videos/` directory into the
container at `/videos`, and reads the required environment variables from
`.env` so the stream starts automatically.

## Note

Make sure you have the rights to broadcast the video content you are streaming to YouTube.
