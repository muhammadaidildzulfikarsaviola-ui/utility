import time
import tkinter as tk


class ProductivityTool:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.remaining = 25 * 60
        self.running = False
        self.job = None
        tk.Label(self.frame, text="Focus Timer", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=(25, 5))
        self.display = tk.Label(self.frame, text="25:00", font=("Segoe UI", 38, "bold"), bg="white")
        self.display.pack(pady=20)
        buttons = tk.Frame(self.frame, bg="white")
        buttons.pack()
        tk.Button(buttons, text="Start", command=self.start).pack(side="left", padx=4)
        tk.Button(buttons, text="Pause", command=self.pause).pack(side="left", padx=4)
        tk.Button(buttons, text="Reset", command=self.reset).pack(side="left", padx=4)

    def start(self):
        if not self.running:
            self.running = True
            self.tick()

    def pause(self):
        self.running = False
        if self.job:
            self.frame.after_cancel(self.job)
            self.job = None

    def reset(self):
        self.pause()
        self.remaining = 25 * 60
        self.update_display()

    def tick(self):
        self.update_display()
        if self.running and self.remaining > 0:
            self.remaining -= 1
            self.job = self.frame.after(1000, self.tick)
        elif self.remaining == 0:
            self.running = False

    def update_display(self):
        minutes, seconds = divmod(self.remaining, 60)
        self.display.config(text=f"{minutes:02d}:{seconds:02d}")
