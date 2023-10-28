import subprocess
import numpy as np

#This is a general DCT class for any array of values
class DCT:
    def __init__(self):
        pass

    def forward_transform(self, data):
        return np.fft.fft2(data)

    def inverse_transform(self, data):
        return np.fft.ifft2(data)

#This DCT class is used for converting JPGs
class DCTConverter:
    def __init__(self):
        pass

    def convert_image_to_dct(self, input_image, output_dct_file):
        try:
            cmd = [
                'ffmpeg',
                '-i', input_image,
                '-vf', 'scale=8x8',
                '-f', 'rawvideo',
                '-pix_fmt', 'gray',
                output_dct_file
            ]
            subprocess.run(cmd, check=True)
            print(f"DCT coefficients extracted and saved as {output_dct_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def convert_dct_to_image(self, input_dct_file, output_image):
        try:
            cmd = [
                'ffmpeg',
                '-s', '8x8',
                '-pix_fmt', 'gray',
                '-f', 'rawvideo',
                '-i', input_dct_file,
                output_image
            ]
            subprocess.run(cmd, check=True)
            print(f"Image reconstructed from DCT coefficients and saved as {output_image}")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


# Example

dct_converter = DCTConverter()

dct_converter.convert_image_to_dct('pepe.jpg', 'dct_coefficients.raw')
dct_converter.convert_dct_to_image('dct_coefficients.raw', 'pepe_dct.jpg')

"We notice that the final result given the original image" \
"is the same as manually running the exersice2" \
"and exersice4 methods"