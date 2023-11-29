import subprocess

def resize_video(input_video, resolution):
    resolutions = {
        "720p": (1280, 720),
        "480p": (854, 480),
        "360x240": (360, 240),
        "160x120": (160, 120)
    }

    output_file = f"{input_video[:-4]}_{resolution}.mp4"

    try:
        size = resolutions.get(resolution)
        if size:
            # Resize video using ffmpeg
            resize_cmd = [
                "ffmpeg",
                "-i", input_video,
                "-vf", f"scale={size[0]}:{size[1]}",
                "-c:a", "copy",
                "-y", output_file
            ]
            subprocess.run(resize_cmd, check=True)

            print(f"Video resized to {resolution}. Output file: {output_file}")
        else:
            print(f"Invalid target resolution: {resolution}. Please choose from: {list(resolutions.keys())}")

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return output_file


def convert_to_format(input_video, format):
    output_file = f"{input_video[:-4]}_{format}.mkv"  # Assume output format is webm for VP8, VP9

    try:
        # Convert video to the specified format using ffmpeg
        convert_cmd = [
            "ffmpeg",
            "-i", input_video,
            "-c:v", format,
            "-c:a", "copy",
            "-y", output_file
        ]
        subprocess.run(convert_cmd, check=True)

        print(f"Video converted to {format}. Output file: {output_file}")
        return output_file

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

class VideoConverter:
    def __init__(self, input_video, resolution, format):
        self.input_video = input_video
        self.resolution = resolution
        self.format = format
        self.resized_video = None

    def process_video(self):
        self.resized_video = resize_video(self.input_video, self.resolution)
        return convert_to_format(self.resized_video, self.format)

# to only resize the video in following resolutions ["720p", "480p", "360x240", "160x120"]
# resize_video("bunny.mp4", "720p")

# to only convert the video in following formats ["vp8", "vp9", "h265", "av1"]
# convert_to_format("bunny.mp4", "vp8")

# automized task
video_converter = VideoConverter("bunny.mp4", "720p", "vp8")
resulting_video = video_converter.process_video()