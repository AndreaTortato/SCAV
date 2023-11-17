import subprocess

#Exercise1
def convert_to_mp2(input_file, output_file):
    try:
        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-c:v", "mpeg2video",
            "-q:v", "2",
            "-c:a", "mp2",
            output_file
        ]
        subprocess.run(cmd, check=True)

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def save_video_info(input_file):
    try:
        cmd = [
            "ffmpeg",
            "-i", input_file
        ]
        #save video info
        info = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        with open("video_info.txt", "w") as info_file:
            info_file.write(info)

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.output}")
    except Exception as e:
        print(f"An error occurred: {e}")


convert_to_mp2("bunny.mp4", "BBB.mp2")
save_video_info("BBB.mp2")

#Exercise2
def modify_resolution(input_file, output_file, resolution):
    try:
        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-vf", f"scale={resolution}",
            output_file
        ]
        subprocess.run(cmd, check=True)
        print(f"Video resolution modified to {resolution}")

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


modify_resolution("bunny.mp4", "bunny_low_res.mp4", "200x600") #to get wierd resolution

#Exercise3
def change_chroma_subsampling(input_file, output_file, subsampling):
    try:
        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-vf", f"format={subsampling}",
            "-c:v", "libx264",
            output_file
        ]
        subprocess.run(cmd, check=True)
        print(f"Chroma subsampling changed to subme={subsampling}")

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


change_chroma_subsampling("bunny.mp4", "bunny_subsamp.mp4", "yuv420p")
#subsampling formats:
# 8-bit 4:2:0: yuv420p
# 8-bit 4:2:2: yuv422p
# 8-bit 4:4:4: yuv444p
# 10-bit 4:2:0: yuv420p10le
# 10-bit 4:2:2: yuv422p10le
# 10-bit 4:4:4: yuv444p10le


#Exercise4
def read_video_info(input_file):
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,codec_name,duration,bit_rate",
            "-of", "default=noprint_wrappers=1:nokey=1",
            input_file
        ]
        video_info = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True).strip().split('\n')

        print("Video Information:")
        print(f"Width: {video_info[0]} pixels")
        print(f"Height: {video_info[1]} pixels")
        print(f"Codec: {video_info[2]}")
        print(f"Duration: {video_info[3]} seconds")
        print(f"Bit Rate: {video_info[4]} bps")
    except subprocess.CalledProcessError as e:
        print(f"FFprobe error: {e.output}")
    except Exception as e:
        print(f"An error occurred: {e}")


read_video_info("bunny.mp4")


#Exercise 5
#Use function from P1 to transform each frame of the video in black and white.
#First we obtain a frame, we tranform it to BnW and then we add them up again
#(not working for now)

import sys
sys.path.insert(1, '../P1/exercise4.py')
from exercise4 import transform_to_BnW

def make_video_BnW(input_file, output_file):
    try:
        temp_frames_txt = 'temp_frames.txt'

        # Create a text file to store the list of transformed frames
        with open(temp_frames_txt, 'w') as file:
            frame_number = 0

            while True:
                input_frame = f'temp_frame_{frame_number}.jpg'
                output_frame = f'temp_frame_BnW_{frame_number}.jpg'

                # Extract the current frame
                extract_frame_cmd = [
                    'ffmpeg',
                    '-i', input_file,
                    '-vf', f'select=gte(n\,{frame_number})',
                    '-vframes', '1',
                    input_frame
                ]
                subprocess.run(extract_frame_cmd, check=True)

                # Transform the current frame
                transform_to_BnW(input_frame, output_frame, quality=2)

                # Write the path of the transformed frame to the text file
                file.write(f"file '{output_frame}'\n")

                frame_number += 1

                # Break the loop if there are no more frames
                if not subprocess.run(['ffmpeg', '-i', input_file], stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).returncode == 0:
                    break

        # Combine the transformed frames into the output video
        combine_cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', temp_frames_txt,
            '-c', 'h264',
            '-pix_fmt', 'yuv420p',
            output_file
        ]
        subprocess.run(combine_cmd, check=True)

        print(f"Black and white video created: {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.output}")
    except Exception as e:
        print(f"An error occurred: {e}")


make_video_BnW("bunny.mp4", "bunny_BnW.mp4")
