import tkinter as tk # sudo apt-get install python3-tk
from tkinter import filedialog
from functools import partial
import threading
import os

import sys
sys.path.insert(1, 'exercise1.py')
from exercise1 import resize_video, convert_to_format

class VideoConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Video Converter")

        self.input_video_path = tk.StringVar()
        self.target_resolution = tk.StringVar()
        self.output_format = tk.StringVar()

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Select Video Button
        self.select_video_button = tk.Button(self.master, text="Select Video", command=self.select_video)
        self.select_video_button.pack()

        # Target Resolution Dropdown
        resolutions = ["720p", "480p", "360x240", "160x120"]
        self.resolution_label = tk.Label(self.master, text="Select Resolution:")
        self.resolution_label.pack()
        self.resolution_dropdown = tk.OptionMenu(self.master, self.target_resolution, *resolutions)
        self.target_resolution.set(resolutions[0])
        self.resolution_dropdown.pack()

        # Output Format Dropdown
        formats = ["vp8", "vp9", "h265", "av1"]
        self.format_label = tk.Label(self.master, text="Select Format:")
        self.format_label.pack()
        self.format_dropdown = tk.OptionMenu(self.master, self.output_format, *formats)
        self.output_format.set(formats[0])
        self.format_dropdown.pack()

        # Play Button
        self.play_button = tk.Button(self.master, text="Play", command=self.play_video)
        self.play_button.pack()

    def select_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.mkv")])
        self.input_video_path.set(file_path)

    def play_video(self):
        input_video = self.input_video_path.get()
        target_resolution = self.target_resolution.get()
        output_format = self.output_format.get()

        if not input_video:
            tk.messagebox.showerror("Error", "Please select a video.")
            return

        if not os.path.isfile(input_video):
            tk.messagebox.showerror("Error", "Invalid file path.")
            return

        # Create a separate thread for the conversion to avoid freezing the GUI
        conversion_thread = threading.Thread(target=self.perform_conversion, args=(input_video, target_resolution, output_format))
        conversion_thread.start()

    def perform_conversion(self, input_video, target_resolution, output_format):
        resized_video = resize_video(input_video, target_resolution)
        if resized_video:
            converted_video = convert_to_format(resized_video, output_format)
            if converted_video:
                tk.messagebox.showinfo("Conversion Complete", f"Video successfully converted to {output_format} format.")
                self.play_converted_video(converted_video)
            else:
                tk.messagebox.showerror("Error", "Video conversion failed.")
        else:
            tk.messagebox.showerror("Error", "Video resizing failed.")

    def play_converted_video(self, video_path):
        os.system(f"ffplay {video_path}")  # Assuming ffplay is available in your system

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()