import subprocess


# Exercise 4

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


transform_to_BnW('pepe.jpg', 'pepe_BnW.jpg', 3)

"The output image has the same quality as the input" \
"image bit it's in black and white"
