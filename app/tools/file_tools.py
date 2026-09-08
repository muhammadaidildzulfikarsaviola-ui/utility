import os
import tkinter as tk
from tkinter import filedialog, messagebox


class FileTools:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.path = tk.StringVar(value="No folder selected")
        tk.Label(self.frame, text="Folder Organizer", font=("Segoe UI", 18, "bold"), bg="white", fg="#202020").pack(anchor="w", padx=20, pady=(20, 5))
        tk.Label(self.frame, textvariable=self.path, bg="white", fg="#666", wraplength=330).pack(anchor="w", padx=20, pady=5)
        tk.Button(self.frame, text="Choose Folder", command=self.choose_folder).pack(anchor="w", padx=20, pady=10)
        self.result = tk.Label(self.frame, text="Select a folder to inspect its contents.", bg="white", fg="#777", justify="left")
        self.result.pack(anchor="w", padx=20, pady=10)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return
        self.path.set(folder)
        files = [name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))]
        folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
        self.result.config(text=f"Files: {len(files)}\nFolders: {len(folders)}\nTotal items: {len(files) + len(folders)}")
