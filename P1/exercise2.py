import subprocess


def resize_and_reduce_quality(input_file, output_file, width, height, quality):
    try:
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-vf', f'scale={width}:{height}',
            '-q:v', str(quality),
            output_file
        ]
        subprocess.run(cmd, check=True)  # to execute the ffmpeg command
        print(f"Image resized and saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


resize_and_reduce_quality('pepe.jpg', 'pepe_low.jpg', 8, 8, 2)

"The output image is reduced in quality and size based on" \
"the given parameters, so there will be an 8x8 output image"