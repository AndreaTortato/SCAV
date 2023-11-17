import subprocess
import json
import sys

#Exercise 1
class MotionVector:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def visualize_motion_vectors(self):
        try:
            cmd = [
                "ffmpeg",
                "-v", "error",
                "-flags2", "+export_mvs",
                "-i", self.input_file,
                "-vf", "codecview=mv=pf+bf+bb",
                "-y", self.output_file
            ]

            subprocess.run(cmd, check=True)
            print(f"Macroblocks and motion vectors visualized and saved to {self.output_file}")
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

#motion_vector_extractor = MotionVector("bunny_9sec.mp4", "bunny_mv.mp4")
#motion_vector_extractor.visualize_motion_vectors()

#Exercise 2
class BBBContainer:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def process_video(self):
        try:
            # Cut video to 50 seconds
            cut_cmd = [
                "ffmpeg",
                "-i", self.input_file,
                "-t", "50",
                "-c", "copy",
                "-y", "50s_cut_video.mp4"
            ]
            subprocess.run(cut_cmd, check=True)

            # Export audio as MP3 mono track
            mp3_mono_cmd = [
                "ffmpeg",
                "-i", "50s_cut_video.mp4",
                "-vn",
                "-ac", "1",
                "-q:a", "2",
                "-y", "audio_mono.mp3"
            ]
            subprocess.run(mp3_mono_cmd, check=True)

            # Export audio in MP3 stereo with lower bitrate
            mp3_stereo_cmd = [
                "ffmpeg",
                "-i", "50s_cut_video.mp4",
                "-vn",
                "-q:a", "5",
                "-y", "audio_stereo.mp3"
            ]
            subprocess.run(mp3_stereo_cmd, check=True)

            # Export audio in AAC codec
            aac_cmd = [
                "ffmpeg",
                "-i", "50s_cut_video.mp4",
                "-vn",
                "-c:a", "aac",
                "-b:a", "128k",
                "-y", "audio_aac.mp4"
            ]
            subprocess.run(aac_cmd, check=True)

            # Package everything into a .mp4
            merge_cmd = [
                "ffmpeg",
                "-i", "50s_cut_video.mp4",
                "-i", "audio_mono.mp3",
                "-i", "audio_stereo.mp3",
                "-c", "copy",
                "-map", "0:v",
                "-map", "1:a",
                "-map", "2:a",
                "-y", self.output_file
            ]
            subprocess.run(merge_cmd, check=True)

            print(f"Processing completed. Output file: {self.output_file}")

        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


#video_processor = BBBContainer("bunny.mp4", "reconstructed_bunny.mp4")
#video_processor.process_video()

#Exercise 3
class MP4ContainerReader:
    def __init__(self, input_file):
        self.input_file = input_file

    def count_tracks(self):
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-print_format", "json",
                "-show_entries", "format=nb_streams",
                self.input_file
            ]

            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
            data = json.loads(output)

            if "format" in data and "nb_streams" in data["format"]:
                num_tracks = int(data["format"]["nb_streams"])
                print(f"The MP4 container contains {num_tracks} tracks.")
            else:
                print("Unable to determine the number of tracks.")

        except subprocess.CalledProcessError as e:
            print(f"FFprobe error: {e.output}")
        except Exception as e:
            print(f"An error occurred: {e}")


#container_reader = MP4ContainerReader("bunny.mp4")
#container_reader.count_tracks() # output says MP4 container contains 2 tracks.


#Exercise 5
sys.path.insert(1, 'exercise4.py')
from exercise4 import VideoWithSubtitles

video_url = "https://www.youtube.com/watch?v=GYlMID6G4Gc"
output_video = "video_with_subtitles.mp4"

video_with_subtitles = VideoWithSubtitles(video_url, output_video)

# Download subtitles not working, there is a problem in reading youtube-dl adn for now I couldn't fix it
# At least it inherits correctly...
#
#if video_with_subtitles.download_subtitles():
#    video_with_subtitles.integrate_subtitles()


#Exercise 6
sys.path.insert(1, 'exercise6.py')
from exercise6 import VideoWithHistogram

video_with_histogram = VideoWithHistogram("bunny.mp4", "histogram_video.mp4")
video_with_histogram.extract_histogram()

