import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class FileTools:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.folder = tk.StringVar(value="")
        self.file_path = tk.StringVar(value="")
        self.new_folder_name = tk.StringVar()
        self.new_file_name = tk.StringVar()
        self.prefix = tk.StringVar()
        self.suffix = tk.StringVar()
        self.start_number = tk.IntVar(value=1)
        self.preview_items = []

        tk.Label(self.frame, text="File Tools", font=("Segoe UI", 18, "bold"), bg="white", fg="#202020").pack(anchor="w", padx=20, pady=(18, 2))
        tk.Label(self.frame, text="Rename one item or batch rename files without leaving Explorer.", bg="white", fg="#777777").pack(anchor="w", padx=20, pady=(0, 12))

        notebook = ttk.Notebook(self.frame)
        notebook.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        folder_tab = tk.Frame(notebook, bg="white")
        file_tab = tk.Frame(notebook, bg="white")
        batch_tab = tk.Frame(notebook, bg="white")
        notebook.add(folder_tab, text="Rename Folder")
        notebook.add(file_tab, text="Rename File")
        notebook.add(batch_tab, text="Batch Rename")

        self._build_folder_tab(folder_tab)
        self._build_file_tab(file_tab)
        self._build_batch_tab(batch_tab)

    def _label(self, parent, text):
        tk.Label(parent, text=text, bg="white", fg="#333333").pack(anchor="w", padx=18, pady=(15, 5))

    def _build_folder_tab(self, parent):
        self._label(parent, "Folder")
        row = tk.Frame(parent, bg="white")
        row.pack(fill="x", padx=18)
        tk.Entry(row, textvariable=self.folder).pack(side="left", fill="x", expand=True)
        tk.Button(row, text="Browse", command=self.choose_folder).pack(side="left", padx=(8, 0))
        self._label(parent, "New folder name")
        tk.Entry(parent, textvariable=self.new_folder_name).pack(fill="x", padx=18)
        tk.Button(parent, text="Rename Folder", command=self.rename_folder).pack(anchor="w", padx=18, pady=15)

    def _build_file_tab(self, parent):
        self._label(parent, "File")
        row = tk.Frame(parent, bg="white")
        row.pack(fill="x", padx=18)
        tk.Entry(row, textvariable=self.file_path).pack(side="left", fill="x", expand=True)
        tk.Button(row, text="Browse", command=self.choose_file).pack(side="left", padx=(8, 0))
        self._label(parent, "New file name")
        tk.Entry(parent, textvariable=self.new_file_name).pack(fill="x", padx=18)
        tk.Label(parent, text="Include the extension if you want to change it. Otherwise it is preserved.", bg="white", fg="#777777", font=("Segoe UI", 8)).pack(anchor="w", padx=18, pady=5)
        tk.Button(parent, text="Rename File", command=self.rename_file).pack(anchor="w", padx=18, pady=15)

    def _build_batch_tab(self, parent):
        self._label(parent, "Folder")
        row = tk.Frame(parent, bg="white")
        row.pack(fill="x", padx=18)
        tk.Entry(row, textvariable=self.folder).pack(side="left", fill="x", expand=True)
        tk.Button(row, text="Browse", command=self.choose_batch_folder).pack(side="left", padx=(8, 0))

        controls = tk.Frame(parent, bg="white")
        controls.pack(fill="x", padx=18, pady=12)
        for column, (label, variable, width) in enumerate((("Prefix", self.prefix, 14), ("Suffix", self.suffix, 14), ("Start", self.start_number, 7))):
            tk.Label(controls, text=label, bg="white").grid(row=0, column=column * 2, sticky="w", padx=(0, 5))
            tk.Entry(controls, textvariable=variable, width=width).grid(row=0, column=column * 2 + 1, sticky="w", padx=(0, 15))
        tk.Button(controls, text="Preview", command=self.preview_batch).grid(row=0, column=6, padx=5)
        tk.Button(controls, text="Apply", command=self.apply_batch).grid(row=0, column=7)

        self.preview = tk.Listbox(parent, font=("Consolas", 9), height=12)
        self.preview.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder.set(folder)

    def choose_batch_folder(self):
        self.choose_folder()
        self.preview_batch()

    def choose_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_path.set(path)

    def rename_folder(self):
        source = self.folder.get().strip()
        name = self.new_folder_name.get().strip()
        if not source or not os.path.isdir(source):
            messagebox.showerror("Rename Folder", "Choose an existing folder first.")
            return
        if not name or os.path.basename(source) == name:
            messagebox.showwarning("Rename Folder", "Enter a different folder name.")
            return
        destination = os.path.join(os.path.dirname(source), name)
        if os.path.exists(destination):
            messagebox.showerror("Rename Folder", "A file or folder with that name already exists.")
            return
        try:
            os.rename(source, destination)
            self.folder.set(destination)
            self.new_folder_name.set("")
            messagebox.showinfo("Rename Folder", "Folder renamed successfully.")
        except OSError as exc:
            messagebox.showerror("Rename Folder", str(exc))

    def rename_file(self):
        source = self.file_path.get().strip()
        name = self.new_file_name.get().strip()
        if not source or not os.path.isfile(source):
            messagebox.showerror("Rename File", "Choose an existing file first.")
            return
        if not name:
            messagebox.showwarning("Rename File", "Enter a new file name.")
            return
        if not os.path.splitext(name)[1]:
            name += os.path.splitext(source)[1]
        destination = os.path.join(os.path.dirname(source), name)
        if os.path.abspath(source) == os.path.abspath(destination):
            return
        if os.path.exists(destination):
            messagebox.showerror("Rename File", "A file with that name already exists.")
            return
        try:
            os.rename(source, destination)
            self.file_path.set(destination)
            self.new_file_name.set("")
            messagebox.showinfo("Rename File", "File renamed successfully.")
        except OSError as exc:
            messagebox.showerror("Rename File", str(exc))

    def preview_batch(self):
        self.preview.delete(0, "end")
        folder = self.folder.get().strip()
        if not os.path.isdir(folder):
            return
        files = sorted(name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name)))
        try:
            number = int(self.start_number.get())
        except (ValueError, tk.TclError):
            number = 1
            self.start_number.set(1)
        self.preview_items = []
        for filename in files:
            stem, extension = os.path.splitext(filename)
            new_name = f"{self.prefix.get()}{number:02d} - {stem}{self.suffix.get()}{extension}"
            self.preview_items.append((filename, new_name))
            self.preview.insert("end", f"{filename}  ->  {new_name}")
            number += 1

    def apply_batch(self):
        self.preview_batch()
        if not self.preview_items:
            messagebox.showwarning("Batch Rename", "No files found in the selected folder.")
            return
        if not messagebox.askyesno("Batch Rename", f"Rename {len(self.preview_items)} file(s)?"):
            return
        folder = self.folder.get().strip()
        destinations = [os.path.join(folder, new) for _, new in self.preview_items]
        if len(set(destinations)) != len(destinations) or any(os.path.exists(path) and path not in [os.path.join(folder, old) for old, _ in self.preview_items] for path in destinations):
            messagebox.showerror("Batch Rename", "The preview contains a name collision. Nothing was changed.")
            return
        try:
            temporary = []
            for index, (old, _) in enumerate(self.preview_items):
                source = os.path.join(folder, old)
                temp = os.path.join(folder, f".__aidil_utility_tmp_{index}__")
                os.rename(source, temp)
                temporary.append((temp, self.preview_items[index][1]))
            for temp, new_name in temporary:
                os.rename(temp, os.path.join(folder, new_name))
            messagebox.showinfo("Batch Rename", f"Renamed {len(temporary)} file(s) successfully.")
            self.preview_batch()
        except OSError as exc:
            messagebox.showerror("Batch Rename", f"Batch rename stopped: {exc}")
