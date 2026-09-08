import subprocess
import tkinter as tk


class WindowsTools:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self._build()

    def _build(self):
        tk.Label(
            self.frame,
            text="Windows Tools",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#202020",
        ).pack(anchor="w", padx=25, pady=(25, 5))

        tk.Label(
            self.frame,
            text="Quick actions for common Windows commands.",
            font=("Segoe UI", 10),
            bg="white",
            fg="#666666",
        ).pack(anchor="w", padx=25, pady=(0, 20))

        actions = tk.Frame(self.frame, bg="white")
        actions.pack(fill="x", padx=25)

        self._button(actions, "Shutdown", self.shutdown)
        self._button(actions, "Restart", self.restart)
        self._button(actions, "Lock PC", self.lock)
        self._button(actions, "Sign Out", self.sign_out)
        self._button(actions, "Hibernate", self.hibernate)

        tk.Label(
            self.frame,
            text="Shutdown delay (seconds)",
            font=("Segoe UI", 9),
            bg="white",
            fg="#555555",
        ).pack(anchor="w", padx=25, pady=(25, 5))

        self.delay = tk.StringVar(value="0")
        tk.Entry(
            self.frame,
            textvariable=self.delay,
            width=12,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=25)

        self.status = tk.Label(
            self.frame,
            text="Ready.",
            font=("Segoe UI", 9),
            bg="white",
            fg="#777777",
        )
        self.status.pack(anchor="w", padx=25, pady=15)

    @staticmethod
    def _button(parent, text, command):
        tk.Button(
            parent,
            text=text,
            command=command,
            relief="flat",
            bg="#eeeeee",
            activebackground="#dddddd",
            padx=14,
            pady=8,
            font=("Segoe UI", 9),
        ).pack(side="left", padx=(0, 8))

    def _seconds(self):
        try:
            value = int(self.delay.get())
            return max(0, min(value, 31536000))
        except ValueError:
            self.status.config(text="Delay must be a whole number.")
            return None

    def shutdown(self):
        seconds = self._seconds()
        if seconds is None:
            return
        subprocess.Popen(["shutdown", "/s", "/t", str(seconds)])
        self.status.config(text=f"Shutdown scheduled in {seconds} second(s).")

    def restart(self):
        subprocess.Popen(["shutdown", "/r", "/t", "0"])

    @staticmethod
    def lock():
        subprocess.Popen(["rundll32.exe", "user32.dll,LockWorkStation"])

    @staticmethod
    def sign_out():
        subprocess.Popen(["shutdown", "/l"])

    @staticmethod
    def hibernate():
        subprocess.Popen(["shutdown", "/h"])
