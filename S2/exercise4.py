import subprocess

#Exercise 4
class VideoWithSubtitles:
    def __init__(self, video_url, output_file):
        self.video_url = video_url
        self.output_file = output_file

    def download_subtitles(self):
        try:
            # Download subtitles using youtube-dl with verbose output
            download_cmd = [
                "youtube-dl",
                "--write-sub",
                "--sub-lang", "en",
                "--skip-download",
                "--quiet",
                "--verbose",
                "-o", "%(id)s.%(ext)s",
                self.video_url
            ]
            subprocess.run(download_cmd, check=True)

        except subprocess.CalledProcessError as e:
            print(f"Error downloading subtitles: {e}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

        return True

    def integrate_subtitles(self):
        try:
            # Integrate subtitles into the video
            integrate_cmd = [
                "ffmpeg",
                "-i", f"{self.video_url.split('=')[1]}.mp4",  # Assuming YouTube video, adjust if needed
                "-vf", "subtitles=en.srt",
                "-c:a", "copy",
                "-y", self.output_file
            ]
            subprocess.run(integrate_cmd, check=True)

            print(f"Video with subtitles saved to {self.output_file}")

        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

