import tkinter as tk

from app.services.system_monitor import SystemMonitor


class Dashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f2f2f2")

        self.monitor = SystemMonitor()
        self.cards = {}

        title = tk.Label(
            self,
            text="Dashboard",
            font=("Segoe UI", 26, "bold"),
            bg="#f2f2f2",
            fg="#202020",
        )
        title.pack(anchor="w", padx=40, pady=(35, 5))

        subtitle = tk.Label(
            self,
            text="Your laptop activity at a glance.",
            font=("Segoe UI", 11),
            bg="#f2f2f2",
            fg="#666666",
        )
        subtitle.pack(anchor="w", padx=40, pady=(0, 25))

        cards = tk.Frame(self, bg="#f2f2f2")
        cards.pack(fill="x", padx=40)

        self.create_card(cards, "CPU", "--", "Current usage")
        self.create_card(cards, "Memory", "--", "Current usage")
        self.create_card(cards, "Disk", "--", "Current usage")
        self.create_card(cards, "Uptime", "--", "Since last boot")

        activity_title = tk.Label(
            self,
            text="Activity tracking",
            font=("Segoe UI", 15, "bold"),
            bg="#f2f2f2",
            fg="#202020",
        )
        activity_title.pack(anchor="w", padx=40, pady=(30, 8))

        self.activity_status = tk.Label(
            self,
            text="Activity database ready. Application tracking will be connected next.",
            font=("Segoe UI", 10),
            bg="#f2f2f2",
            fg="#777777",
        )
        self.activity_status.pack(anchor="w", padx=40)

        self.refresh()

    def create_card(self, parent, title, value, description):
        card = tk.Frame(parent, bg="white", height=105)
        card.pack(side="left", fill="x", expand=True, padx=(0, 8))
        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 10),
            bg="white",
            fg="#777777",
        ).pack(anchor="w", padx=18, pady=(14, 0))

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#202020",
        )
        value_label.pack(anchor="w", padx=18)

        tk.Label(
            card,
            text=description,
            font=("Segoe UI", 8),
            bg="white",
            fg="#999999",
        ).pack(anchor="w", padx=18)

        self.cards[title] = value_label

    def refresh(self):
        values = {
            "CPU": self.monitor.cpu_percent(),
            "Memory": self.monitor.memory_percent(),
            "Disk": self.monitor.disk_percent(),
            "Uptime": self.format_uptime(self.monitor.uptime_seconds()),
        }

        for title, value in values.items():
            if value is None:
                display = "Install psutil"
            elif title == "Uptime":
                display = value
            else:
                display = f"{value:.0f}%"
            self.cards[title].config(text=display)

        self.after(1500, self.refresh)

    @staticmethod
    def format_uptime(seconds):
        if seconds is None:
            return "--"

        seconds = int(seconds)
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, _ = divmod(seconds, 60)

        if days:
            return f"{days}d {hours}h"
        if hours:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"
