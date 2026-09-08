import os
import subprocess
import tkinter as tk
from tkinter import messagebox


class WindowsTools:
    """GUI wrappers for common Windows power and session commands."""

    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.delay = tk.IntVar(value=0)

        tk.Label(self.frame, text="Windows Tools", font=("Segoe UI", 18, "bold"), bg="white", fg="#202020").pack(anchor="w", padx=20, pady=(20, 3))
        tk.Label(self.frame, text="Quick controls for common Windows commands.", font=("Segoe UI", 9), bg="white", fg="#777777").pack(anchor="w", padx=20, pady=(0, 18))

        actions = tk.Frame(self.frame, bg="white")
        actions.pack(fill="x", padx=20)
        self._button(actions, "Shutdown", self.schedule_shutdown, 0, 0)
        self._button(actions, "Restart", self.restart, 0, 1)
        self._button(actions, "Lock PC", self.lock_pc, 1, 0)
        self._button(actions, "Sign Out", self.sign_out, 1, 1)
        self._button(actions, "Hibernate", self.hibernate, 2, 0)
        self._button(actions, "Cancel Shutdown", self.cancel_shutdown, 2, 1)

        timer = tk.LabelFrame(self.frame, text="Shutdown Timer", bg="white", fg="#333333", font=("Segoe UI", 9, "bold"))
        timer.pack(fill="x", padx=20, pady=22)
        row = tk.Frame(timer, bg="white")
        row.pack(fill="x", padx=12, pady=12)
        tk.Label(row, text="Seconds:", bg="white", fg="#333333").pack(side="left")
        tk.Spinbox(row, from_=0, to=86400, textvariable=self.delay, width=8).pack(side="left", padx=8)
        tk.Button(row, text="Schedule Shutdown", command=self.schedule_shutdown).pack(side="left")

        self.command_text = tk.StringVar(value="Command preview: shutdown /s /t 0")
        tk.Label(timer, textvariable=self.command_text, bg="white", fg="#666666", font=("Consolas", 9)).pack(anchor="w", padx=12, pady=(0, 12))
        self.delay.trace_add("write", self.update_preview)

    def _button(self, parent, text, command, row, column):
        button = tk.Button(parent, text=text, command=command, font=("Segoe UI", 10), relief="flat", bg="#eeeeee", activebackground="#dddddd", padx=12, pady=10)
        button.grid(row=row, column=column, sticky="ew", padx=4, pady=4)
        parent.grid_columnconfigure(column, weight=1)

    def run_command(self, args):
        if os.name != "nt":
            messagebox.showwarning("Windows only", "This action is available on Windows.")
            return False
        try:
            subprocess.Popen(args, shell=False)
            return True
        except OSError as exc:
            messagebox.showerror("Windows command failed", str(exc))
            return False

    def schedule_shutdown(self):
        try:
            seconds = max(0, int(self.delay.get()))
        except (ValueError, tk.TclError):
            seconds = 0
            self.delay.set(0)
        if messagebox.askyesno("Schedule Shutdown", f"Schedule Windows shutdown in {seconds} second(s)?"):
            self.run_command(["shutdown", "/s", "/t", str(seconds)])

    def restart(self):
        if messagebox.askyesno("Restart PC", "Restart Windows now?"):
            self.run_command(["shutdown", "/r", "/t", "0"])

    def cancel_shutdown(self):
        if messagebox.askyesno("Cancel Shutdown", "Cancel a pending Windows shutdown?"):
            self.run_command(["shutdown", "/a"])

    def lock_pc(self):
        self.run_command(["rundll32.exe", "user32.dll,LockWorkStation"])

    def sign_out(self):
        if messagebox.askyesno("Sign Out", "Sign out of Windows now?"):
            self.run_command(["shutdown", "/l"])

    def hibernate(self):
        if messagebox.askyesno("Hibernate", "Hibernate Windows now?"):
            self.run_command(["shutdown", "/h"])

    def update_preview(self, *_):
        try:
            seconds = max(0, int(self.delay.get()))
        except (ValueError, tk.TclError):
            seconds = 0
        self.command_text.set(f"Command preview: shutdown /s /t {seconds}")
