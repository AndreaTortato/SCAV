import subprocess

def read_jpeg_bytes(file_path):
    try:
        with open(file_path, 'rb') as jpeg_file:
            jpeg_bytes = bytearray()

            # to get height and width of the image
            try:
                cmd = [
                    "ffprobe",
                    "-v", "error",
                    "-select_streams", "v:0",
                    "-show_entries", "stream=width,height",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    file_path
                ]
                output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
                width, height = map(int, output.strip().split())

            except subprocess.CalledProcessError as e:
                print(f"FFmpeg error: {e.output}")
            except Exception as e:
                print(f"An error occurred: {e}")

            indices = [i for i in range(width * height)]
            for index in indices:
                jpeg_file.seek(index)
                byte = jpeg_file.read(1)
                jpeg_bytes.extend(byte)

            return jpeg_bytes

    except FileNotFoundError:
        return None

def read_jpeg_serpentine(file_path):
    try:
        with open(file_path, 'rb') as jpeg_file:

            # to get height and width of the image
            try:
                cmd = [
                    "ffprobe",
                    "-v", "error",
                    "-select_streams", "v:0",
                    "-show_entries", "stream=width,height",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    file_path
                ]
                output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
                width, height = map(int, output.strip().split())

            except subprocess.CalledProcessError as e:
                print(f"FFmpeg error: {e.output}")
            except Exception as e:
                print(f"An error occurred: {e}")

            serpetine_indices = [i for i in range(width*height)]
            serpetine_indices.sort(key=lambda x: (x % 10, x // 10))  # Change the sorting pattern as needed

            # Read bytes in the zigzag pattern
            serpetine_bytes = bytearray()
            for index in serpetine_indices:
                jpeg_file.seek(index)
                byte = jpeg_file.read(1)
                serpetine_bytes.extend(byte)

            return serpetine_bytes

    except FileNotFoundError:
        return None



print('image bytes in order: ', read_jpeg_bytes('pepe_low.jpg'), '\n')
print('image bytes in serpentine order: ',read_jpeg_serpentine('pepe_low.jpg'))
