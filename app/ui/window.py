import json
import os
import tkinter as tk

from app.ui.sidebar import Sidebar
from app.ui.dashboard import Dashboard
from app.ui.floating_window import FloatingWindow


class UtilityApp:
    STATE_FILE = os.path.join("data", "window_state.json")

    def __init__(self, root):
        self.root = root
        self.root.title("Aidil Utility")
        self.root.geometry("1100x700")
        self.root.minsize(850, 550)
        self.root.configure(bg="#f2f2f2")

        self.floating_windows = {}
        self.window_state = self.load_window_state()

        self.sidebar = Sidebar(
            self.root,
            on_page_change=self.open_tool
        )
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self.root, bg="#f2f2f2")
        self.content.pack(side="right", fill="both", expand=True)

        self.dashboard = Dashboard(self.content)
        self.dashboard.pack(fill="both", expand=True)

    def load_window_state(self):
        try:
            with open(self.STATE_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return {}

    def save_window_state(self, tool_name, window):
        os.makedirs(os.path.dirname(self.STATE_FILE), exist_ok=True)
        self.window_state[tool_name] = {
            "geometry": window.get_geometry(),
            "always_on_top": window.always_on_top.get(),
        }

        try:
            with open(self.STATE_FILE, "w", encoding="utf-8") as file:
                json.dump(self.window_state, file, indent=2)
        except OSError:
            pass

    def open_tool(self, tool_name):
        if tool_name == "Dashboard":
            self.show_dashboard()
            return

        if tool_name in self.floating_windows:
            window = self.floating_windows[tool_name]
            if window.winfo_exists():
                window.deiconify()
                window.lift()
                window.focus_force()
                return

        state = self.window_state.get(tool_name, {})
        geometry = state.get("geometry", "400x300")
        always_on_top = state.get("always_on_top", False)

        window = FloatingWindow(
            self.root,
            title=tool_name,
            on_close=lambda closed_window, name=tool_name: self.close_tool(
                name, closed_window
            ),
            geometry=geometry,
            always_on_top=always_on_top,
        )

        self.floating_windows[tool_name] = window
        self.create_tool_content(window, tool_name)

    def create_tool_content(self, window, tool_name):
        title = tk.Label(
            window.content,
            text=tool_name,
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#202020",
        )
        title.pack(anchor="w", padx=25, pady=(25, 5))

        description = tk.Label(
            window.content,
            text="Utility panel is ready.",
            font=("Segoe UI", 10),
            bg="white",
            fg="#666666",
        )
        description.pack(anchor="w", padx=25)

    def close_tool(self, tool_name, window):
        self.save_window_state(tool_name, window)
        self.floating_windows.pop(tool_name, None)

    def show_dashboard(self):
        self.dashboard.lift()
        self.root.lift()

    def run(self):
        self.root.mainloop()
