import tkinter as tk

from app.ui.sidebar import Sidebar
from app.ui.dashboard import Dashboard
from app.ui.floating_window import FloatingWindow


class UtilityApp:
    def __init__(self, root):
        self.root = root

        self.root.title("Aidil Utility")
        self.root.geometry("1100x700")
        self.root.minsize(850, 550)

        self.root.configure(bg="#f2f2f2")

        self.floating_windows = {}

        self.sidebar = Sidebar(
            self.root,
            on_page_change=self.open_tool
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.content = tk.Frame(
            self.root,
            bg="#f2f2f2"
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.dashboard = Dashboard(
            self.content
        )

        self.dashboard.pack(
            fill="both",
            expand=True
        )

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

        window = FloatingWindow(
            self.root,
            title=tool_name,
            on_close=lambda: self.remove_window(tool_name)
        )

        self.floating_windows[tool_name] = window

        self.create_tool_content(
            window,
            tool_name
        )

    def create_tool_content(self, window, tool_name):

        title = tk.Label(
            window.content,
            text=tool_name,
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#202020"
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        description = tk.Label(
            window.content,
            text="Utility panel is ready.",
            font=("Segoe UI", 10),
            bg="white",
            fg="#666666"
        )

        description.pack(
            anchor="w",
            padx=25
        )

    def remove_window(self, tool_name):

        if tool_name in self.floating_windows:
            del self.floating_windows[tool_name]

    def show_dashboard(self):

        for window in self.floating_windows.values():

            if window.winfo_exists():
                window.lift()

        self.dashboard.lift()

    def run(self):
        self.root.mainloop()