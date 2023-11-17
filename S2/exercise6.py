import subprocess

#Exercise 6
class VideoWithHistogram:
    def __init__(self, input_video, output_video):
        self.input_video = input_video
        self.output_video = output_video

    def extract_histogram(self):
        try:
            # Extract YUV histogram using ffmpeg
            extract_cmd = [
                "ffmpeg",
                "-i", self.input_video,
                "-vf", "split=2[a][b],[b]histeq[hist],[a][hist]overlay=format=yuv420",
                "-c:a", "copy",
                "-y", self.output_video
            ]
            subprocess.run(extract_cmd, check=True)

            print(f"Histogram extracted and saved to {self.output_video}")

        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
