import os
import subprocess
import tkinter as tk
from tkinter import filedialog

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Caption Generator")
        self.master.geometry("300x200")

        # Lyrics file label and button
        self.lyrics_label = tk.Label(text="Select lyrics file:")
        self.lyrics_label.pack(pady=10)

        self.lyrics_button = tk.Button(text="Browse...", command=self.select_lyrics_file)
        self.lyrics_button.pack()

        # Audio file label and button
        self.audio_label = tk.Label(text="Select audio file:")
        self.audio_label.pack(pady=10)

        self.audio_button = tk.Button(text="Browse...", command=self.select_audio_file)
        self.audio_button.pack()

        # Generate captions button
        self.generate_button = tk.Button(text="Generate captions", command=self.generate_captions)
        self.generate_button.pack(pady=10)

    def select_lyrics_file(self):
        filename = filedialog.askopenfilename(title="Select lyrics file", filetypes=[("Text Files", "*.txt")])
        if filename:
            self.lyrics_file = filename

    def select_audio_file(self):
        filename = filedialog.askopenfilename(title="Select audio file", filetypes=[("Audio Files", "*.wav")])
        if filename:
            self.audio_file = filename

    def generate_captions(self):
        if hasattr(self, 'lyrics_file') and hasattr(self, 'audio_file'):
            subprocess.run(['python', 'txt2captions.py', self.lyrics_file, self.audio_file])
            os.startfile('captions.txt')
        else:
            tk.messagebox.showerror(title="Error", message="Please select both a lyrics file and an audio file.")

root = tk.Tk()
app = App(root)
root.mainloop()
