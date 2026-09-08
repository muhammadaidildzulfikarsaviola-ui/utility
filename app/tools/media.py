import os
import tkinter as tk
from tkinter import filedialog


class MediaTool:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        tk.Label(self.frame, text="Media Info", font=("Segoe UI", 18, "bold"), bg="white").pack(anchor="w", padx=20, pady=(20, 5))
        tk.Button(self.frame, text="Inspect File", command=self.inspect).pack(anchor="w", padx=20, pady=15)
        self.result = tk.Label(self.frame, text="Choose a media file to inspect its basic metadata.", bg="white", fg="#666", justify="left")
        self.result.pack(anchor="w", padx=20)

    def inspect(self):
        path = filedialog.askopenfilename(filetypes=[("Media files", "*.mp3 *.wav *.flac *.mp4 *.mkv *.jpg *.jpeg *.png"), ("All files", "*.*")])
        if not path:
            return
        size = os.path.getsize(path)
        self.result.config(text=f"Name: {os.path.basename(path)}\nSize: {size / 1024 / 1024:.2f} MB\nType: {os.path.splitext(path)[1] or 'Unknown'}")
