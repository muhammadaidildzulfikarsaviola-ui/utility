import tkinter as tk

from app.services.system_monitor import SystemMonitor


class PCMonitorTool:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.monitor = SystemMonitor()
        self.values = {}
        for title in ("CPU", "Memory", "Disk", "Uptime"):
            row = tk.Frame(self.frame, bg="white")
            row.pack(fill="x", padx=25, pady=8)
            tk.Label(row, text=title, width=12, anchor="w", bg="white", fg="#666", font=("Segoe UI", 10)).pack(side="left")
            value = tk.Label(row, text="--", anchor="e", bg="white", fg="#202020", font=("Segoe UI", 13, "bold"))
            value.pack(side="right")
            self.values[title] = value
        self.refresh()

    def refresh(self):
        metrics = {
            "CPU": self.monitor.cpu_percent(),
            "Memory": self.monitor.memory_percent(),
            "Disk": self.monitor.disk_percent(),
            "Uptime": self.format_uptime(self.monitor.uptime_seconds()),
        }
        for name, value in metrics.items():
            if value is None:
                text = "N/A"
            elif name == "Uptime":
                text = value
            else:
                text = f"{value:.1f}%"
            self.values[name].config(text=text)
        self.frame.after(1500, self.refresh)

    @staticmethod
    def format_uptime(seconds):
        if seconds is None:
            return "--"
        days, rem = divmod(int(seconds), 86400)
        hours, rem = divmod(rem, 3600)
        minutes, _ = divmod(rem, 60)
        return f"{days}d {hours}h {minutes}m" if days else f"{hours}h {minutes}m"
