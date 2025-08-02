import subprocess
import sys
import os
import tempfile
import json
from overlay_creator import generate_overlay

def timestamp_to_seconds(t):
    parts = t.split(":")
    parts = [0] * (3 - len(parts)) + list(map(float, parts))
    return parts[0] * 3600 + parts[1] * 60 + parts[2]

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        # When running packaged .exe
        return os.path.join(sys._MEIPASS, "ffmpeg.exe") if hasattr(sys, "_MEIPASS") else "ffmpeg.exe"
    else:
        # When running as standalone script
        return "ffmpeg"

def get_video_resolution(ffmpeg_path, input_path):
    ffprobe_path = ffmpeg_path.replace("ffmpeg", "ffprobe")

    cmd = [
        ffprobe_path,
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "json",
        input_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    info = json.loads(result.stdout)
    width = info["streams"][0]["width"]
    height = info["streams"][0]["height"]
    return width, height

def process_video(video_start, video_end, song_id, input_path="input.mp4", output_path="output.mp4", apply_overlay=True, saturation=1.4):
    # 1: Get initial variables
    width, height = get_video_resolution(get_ffmpeg_path(), input_path)
    duration = timestamp_to_seconds(video_end) - timestamp_to_seconds(video_start)
    fade_out_time = duration - 1

    # 2: Build video filter graph
    video_filter = f"fade=t=in:st=0:d=1,fade=t=out:st={fade_out_time}:d=1"

    if saturation > 1.0:
        video_filter += f",eq=saturation={saturation}"

    video_filter += "[v0]"

    # 3: Generate overlay and build overlay filter graph
    if apply_overlay:
        overlay_path = os.path.join(tempfile.gettempdir(), f"overlay_{song_id}.png")
        generate_overlay(song_id, output_path=overlay_path, width=width, height=height)

        overlay_filter = (
            f"[v0][1:v] overlay="
            "x='if(lt(t,3), -W, if(lt(t,3.5), -W + (t-3)*W*2, if(lt(t,7.5), 0, - (t-7.5)*W*2)))'"
            ":y=0:format=auto[outv]"
        )

        filter_complex = f"[0:v]{video_filter};{overlay_filter}"

        ffmpeg_path = get_ffmpeg_path()

        cmd = [
            ffmpeg_path,
            "-y",
            "-ss", str(video_start),
            "-t", str(duration),
            "-i", input_path,
            "-loop", "1", "-t", "10", "-i", overlay_path,
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-crf", "18",
            "-preset", "medium",
            "-movflags", "+faststart",
            output_path
        ]
    else:
        # 3 (alternative): or skip the overlay and just go straight to processing the video
        filter_complex = f"[0:v]{video_filter};[v0]copy[outv]"

        ffmpeg_path = get_ffmpeg_path()

        cmd = [
            ffmpeg_path,
            "-y",
            "-ss", str(video_start),
            "-t", str(duration),
            "-i", input_path,
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-crf", "18",
            "-preset", "medium",
            "-movflags", "+faststart",
            output_path
        ]

    print("Running FFmpeg...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)
    print("Video processing complete. Output saved as output.mp4")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Use gui.py to generate processing command")
        sys.exit(1)

    video_start = sys.argv[1]
    video_end = sys.argv[2]
    song_id = sys.argv[3]

    process_video(video_start, video_end, song_id)