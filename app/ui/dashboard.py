import tkinter as tk

from app.services.activity_tracker import ActivityTracker
from app.services.system_monitor import SystemMonitor


class Dashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f2f2f2")
        self.monitor = SystemMonitor()
        self.tracker = ActivityTracker()
        self.cards = {}

        tk.Label(
            self, text="Dashboard", font=("Segoe UI", 26, "bold"),
            bg="#f2f2f2", fg="#202020"
        ).pack(anchor="w", padx=40, pady=(30, 3))
        tk.Label(
            self, text="Your laptop activity at a glance.",
            font=("Segoe UI", 11), bg="#f2f2f2", fg="#666666"
        ).pack(anchor="w", padx=40, pady=(0, 20))

        cards = tk.Frame(self, bg="#f2f2f2")
        cards.pack(fill="x", padx=40)
        self.create_card(cards, "CPU", "--", "Current usage")
        self.create_card(cards, "Memory", "--", "Current usage")
        self.create_card(cards, "Disk", "--", "Current usage")
        self.create_card(cards, "Uptime", "--", "Since last boot")

        activity = tk.Frame(self, bg="#f2f2f2")
        activity.pack(fill="both", expand=True, padx=40, pady=(24, 0))

        left = tk.Frame(activity, bg="white")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(
            left, text="Today's activity", font=("Segoe UI", 14, "bold"),
            bg="white", fg="#202020"
        ).pack(anchor="w", padx=18, pady=(16, 2))
        self.activity_value = tk.Label(
            left, text="--", font=("Segoe UI", 24, "bold"),
            bg="white", fg="#202020"
        )
        self.activity_value.pack(anchor="w", padx=18)
        self.activity_detail = tk.Label(
            left, text="Starting tracker...", font=("Segoe UI", 9),
            bg="white", fg="#777777"
        )
        self.activity_detail.pack(anchor="w", padx=18, pady=(0, 8))

        self.chart = tk.Canvas(left, height=150, bg="white", highlightthickness=0)
        self.chart.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.chart.bind("<Configure>", lambda _event: self.draw_chart())
        self.daily_data = []

        right = tk.Frame(activity, bg="white", width=250)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)
        tk.Label(
            right, text="Most used today", font=("Segoe UI", 14, "bold"),
            bg="white", fg="#202020"
        ).pack(anchor="w", padx=18, pady=(16, 10))
        self.top_app = tk.Label(
            right, text="No activity yet", font=("Segoe UI", 13, "bold"),
            bg="white", fg="#202020", wraplength=210, justify="left"
        )
        self.top_app.pack(anchor="w", padx=18)
        self.top_app_time = tk.Label(
            right, text="", font=("Segoe UI", 9), bg="white", fg="#777777"
        )
        self.top_app_time.pack(anchor="w", padx=18, pady=(2, 18))
        tk.Label(
            right, text="Recent apps", font=("Segoe UI", 10, "bold"),
            bg="white", fg="#555555"
        ).pack(anchor="w", padx=18, pady=(0, 5))
        self.apps_label = tk.Label(
            right, text="", font=("Segoe UI", 9), bg="white", fg="#666666",
            justify="left", anchor="nw"
        )
        self.apps_label.pack(fill="both", expand=True, padx=18, pady=(0, 16), anchor="nw")

        self.status = tk.Label(
            self, text="", font=("Segoe UI", 9),
            bg="#f2f2f2", fg="#888888"
        )
        self.status.pack(anchor="w", padx=40, pady=(8, 14))
        self.refresh()

    def create_card(self, parent, title, value, description):
        card = tk.Frame(parent, bg="white", height=100)
        card.pack(side="left", fill="x", expand=True, padx=(0, 8))
        card.pack_propagate(False)
        tk.Label(card, text=title, font=("Segoe UI", 10), bg="white", fg="#777777").pack(anchor="w", padx=18, pady=(12, 0))
        value_label = tk.Label(card, text=value, font=("Segoe UI", 20, "bold"), bg="white", fg="#202020")
        value_label.pack(anchor="w", padx=18)
        tk.Label(card, text=description, font=("Segoe UI", 8), bg="white", fg="#999999").pack(anchor="w", padx=18)
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

        active_app = self.tracker.poll()
        total = self.tracker.get_today_total_seconds()
        sessions = self.tracker.get_today_session_count()
        top_name, top_seconds = self.tracker.get_top_app()
        self.activity_value.config(text=self.tracker.format_duration(total))
        self.activity_detail.config(
            text=f"{sessions} session(s) today  •  {('Active: ' + active_app) if active_app else 'Idle'}"
        )
        if top_name:
            self.top_app.config(text=top_name)
            self.top_app_time.config(text=self.tracker.format_duration(top_seconds))
        else:
            self.top_app.config(text="No activity yet")
            self.top_app_time.config(text="")

        apps = self.tracker.get_recent_apps(5)
        self.apps_label.config(
            text="\n".join(f"{name}   {self.tracker.format_duration(seconds)}" for name, seconds in apps)
            if apps else "No recorded apps yet"
        )
        self.daily_data = self.tracker.get_daily_usage(7)
        self.draw_chart()
        if self.tracker.is_supported():
            self.status.config(text="Activity tracking is running locally. Idle time is excluded.")
        else:
            self.status.config(text="Activity tracking requires Windows + psutil.")
        self.after(2000, self.refresh)

    def draw_chart(self):
        self.chart.delete("all")
        if not self.daily_data:
            return
        width = max(240, self.chart.winfo_width())
        height = max(100, self.chart.winfo_height())
        max_value = max([value for _, value in self.daily_data] + [3600])
        bar_width = max(18, (width - 35) / len(self.daily_data) - 10)
        baseline = height - 28
        for index, (label, seconds) in enumerate(self.daily_data):
            x = 22 + index * ((width - 30) / len(self.daily_data))
            bar_height = (seconds / max_value) * (height - 55)
            self.chart.create_rectangle(x, baseline - bar_height, x + bar_width, baseline, fill="#4f46e5", outline="")
            self.chart.create_text(x + bar_width / 2, baseline + 12, text=label, font=("Segoe UI", 8), fill="#777777")
            if seconds:
                self.chart.create_text(x + bar_width / 2, baseline - bar_height - 8, text=self.tracker.format_duration(seconds), font=("Segoe UI", 7), fill="#555555")
        self.chart.create_line(18, baseline, width - 10, baseline, fill="#dddddd")

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
