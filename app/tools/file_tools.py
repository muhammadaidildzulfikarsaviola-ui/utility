import os
import tkinter as tk
from tkinter import filedialog, messagebox


class FileTools:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.folder = tk.StringVar()
        self.new_name = tk.StringVar()
        self._build()

    def _build(self):
        tk.Label(self.frame, text="File Tools", font=("Segoe UI", 20, "bold"), bg="white", fg="#202020").pack(anchor="w", padx=25, pady=(25, 5))
        tk.Label(self.frame, text="Small file operations without opening five Explorer windows.", font=("Segoe UI", 10), bg="white", fg="#666666").pack(anchor="w", padx=25, pady=(0, 20))
        tk.Label(self.frame, text="Rename folder", font=("Segoe UI", 13, "bold"), bg="white", fg="#202020").pack(anchor="w", padx=25)
        row = tk.Frame(self.frame, bg="white")
        row.pack(fill="x", padx=25, pady=8)
        tk.Entry(row, textvariable=self.folder, font=("Segoe UI", 10)).pack(side="left", fill="x", expand=True)
        tk.Button(row, text="Browse", command=self.browse, relief="flat", bg="#eeeeee").pack(side="left", padx=8)
        tk.Label(self.frame, text="New folder name", font=("Segoe UI", 9), bg="white", fg="#555555").pack(anchor="w", padx=25, pady=(10, 3))
        tk.Entry(self.frame, textvariable=self.new_name, font=("Segoe UI", 10)).pack(fill="x", padx=25)
        tk.Button(self.frame, text="Rename", command=self.rename_folder, relief="flat", bg="#eeeeee", padx=14, pady=7).pack(anchor="w", padx=25, pady=12)
        self.status = tk.Label(self.frame, text="Ready.", font=("Segoe UI", 9), bg="white", fg="#777777")
        self.status.pack(anchor="w", padx=25)

    def browse(self):
        selected = filedialog.askdirectory(title="Select folder")
        if selected:
            self.folder.set(selected)

    def rename_folder(self):
        source = self.folder.get().strip()
        name = self.new_name.get().strip()
        if not source or not os.path.isdir(source):
            self.status.config(text="Select an existing folder first.")
            return
        if not name or name in {".", ".."} or any(char in name for char in '<>:"/\\|?*'):
            self.status.config(text="Enter a valid folder name.")
            return
        destination = os.path.join(os.path.dirname(source), name)
        if os.path.exists(destination):
            self.status.config(text="A file or folder with that name already exists.")
            return
        try:
            os.rename(source, destination)
            self.folder.set(destination)
            self.status.config(text="Folder renamed successfully.")
        except OSError as error:
            messagebox.showerror("Rename failed", str(error))
