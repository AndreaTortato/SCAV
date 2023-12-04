# this file is used to copy files from other exercises, in part since the user might not have the fucntions of
# other files I have and in part since inheritance from anotehr project isn't working
import subprocess

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

def transform_to_BnW(input_file, output_file, quality):
    try:
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-vf', 'format=gray',
            '-q:v', str(quality),
            output_file
        ]
        subprocess.run(cmd, check=True)  # to execute the ffmpeg command
        print(f"Image resized and saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

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

def visualize_motion_vectors(input_file, output_file):
    try:
        cmd = [
            "ffmpeg",
            "-v", "error",
            "-flags2", "+export_mvs",
            "-i", input_file,
            "-vf", "codecview=mv=pf+bf+bb",
            "-y", output_file
        ]

        subprocess.run(cmd, check=True)
        print(f"Macroblocks and motion vectors visualized and saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")