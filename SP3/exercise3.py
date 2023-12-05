import tkinter as tk # sudo apt-get install python3-tk
from tkinter import filedialog
from tkVideoPlayer.tkvideoplayer import TkinterVideo # pip install tkVideoPlayer, to play the video in the app
import os
import time
import subprocess

import sys
sys.path.insert(1, 'exercise1.py')
from exercise1 import VideoConverter
sys.path.insert(1, 'imported_exs.py')
from imported_exs import convert_to_mp2, change_chroma_subsampling, make_video_BnW, visualize_motion_vectors

class VideoConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Video Converter")

        # initial size of the window
        master.geometry("848x480")
        root.configure(bg="#ffcc00")

        # Get the repository root path
        self.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        self.input_video_path = tk.StringVar()
        self.target_resolution = tk.StringVar()
        self.output_format = tk.StringVar()
        self.selected_option = tk.StringVar()

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):

        # play/pause button
        self.play_pause_button_text = tk.StringVar()
        self.play_pause_button_text.set("Pause")
        self.play_pause_button = tk.Button(self.master, textvariable=self.play_pause_button_text,
                                           command=self.toggle_play_pause)
        self.play_pause_button.pack(side=tk.BOTTOM, anchor=tk.SW, padx=10, pady=10)

        # Video Player
        self.video_player = TkinterVideo(master=self.master, scaled=True)
        self.video_player.pack(side=tk.BOTTOM, expand=True, fill="both", padx=10, pady=10)

        # Other options
        actions = ["Options", "Return motion vectors", "Convert to B&W", "Convert to MP2", "Change Chroma SubSamp."]
        self.option_button = tk.Button(self.master, text="Accept option", command=self.select_option)
        self.option_button.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=10)
        self.option_dropdown = tk.OptionMenu(self.master, self.selected_option, *actions)
        self.selected_option.set(actions[0])
        self.option_dropdown.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=10)

        # Select Video Button
        self.select_video_button = tk.Button(self.master, text="Select Video", command=self.select_video)
        self.select_video_button.pack(side=tk.LEFT, anchor=tk.W, padx=10, pady=10)  # to position the widgets

        # Target Resolution Dropdown
        resolutions = ["720p", "480p", "360x240", "160x120"]
        self.resolution_label = tk.Label(self.master, text="Resolution:")
        self.resolution_label.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)
        self.resolution_dropdown = tk.OptionMenu(self.master, self.target_resolution, *resolutions)
        self.target_resolution.set(resolutions[0])
        self.resolution_dropdown.pack(side=tk.LEFT, anchor=tk.NW, padx=0, pady=8)

        # Output Format Dropdown
        formats = ["vp8", "vp9", "h265", "av1"]
        self.format_label = tk.Label(self.master, text="Format:")
        self.format_label.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)
        self.format_dropdown = tk.OptionMenu(self.master, self.output_format, *formats)
        self.output_format.set(formats[0])
        self.format_dropdown.pack(side=tk.LEFT, anchor=tk.NW, padx=0, pady=8)

        # Convert video
        self.convert_button = tk.Button(self.master, text="Convert video", command=self.convert_video)
        self.convert_button.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)

    def select_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.mkv")])
        if file_path:

            # Get the relative path from the repository root
            relative_path = os.path.relpath(file_path, start=self.repo_root)

            # Set the relative path to self.input_video_path
            self.input_video_path.set(relative_path)
            print(f"Selected video: {relative_path}")

            self.video_player.load(file_path)
            self.video_player.play()

    def select_option(self):

        option = self.selected_option.get()
        input_video_path = self.input_video_path.get()

        print(input_video_path)

        if option == "Return motion vectors":
            visualize_motion_vectors(input_video_path, "MV_"+input_video_path)

        elif option == "Convert to B&W":
            make_video_BnW(input_video_path, "B&W_"+input_video_path)

        elif option == "Convert to MP2":
            convert_to_mp2(input_video_path, "mp2"+input_video_path)

        elif option == "Change Chroma SubSamp":
            change_chroma_subsampling(input_video_path, "new_ChromaSS_"+input_video_path, "yuv420p")

    def toggle_play_pause(self):
        if self.video_player.is_paused():
            self.video_player.play()
            self.play_pause_button_text.set("Pause")
        else:
            self.video_player.pause()
            self.play_pause_button_text.set("Play")

    def convert_video(self):
        # Get selected resolution and format
        resolution = self.target_resolution.get()
        format = self.output_format.get()

        # Check if both resolution and format are selected
        if not resolution:
            resolution = "720p"
        if not format:
            format = "vp8"

        input_video_path = self.input_video_path.get()

        video_converter = VideoConverter(input_video_path, resolution, format)
        converted_video = video_converter.process_video()

        self.video_player.pause() #pause current video for loading
        print("Converting video, please wait...")

        i = 0
        # Check if the converted video file exists
        while not os.path.exists(converted_video):
            time.sleep(1)

        if i < 180:
            print("Video conversion completed!")

            # Play the final video
            self.video_player.load(converted_video)
            self.video_player.play()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()