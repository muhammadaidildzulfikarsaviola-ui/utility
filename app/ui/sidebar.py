import tkinter as tk


class Sidebar(tk.Frame):

    def __init__(self, parent, on_page_change):

        super().__init__(
            parent,
            width=220,
            bg="#1f1f1f"
        )

        self.on_page_change = on_page_change

        self.pack_propagate(False)

        title = tk.Label(
            self,
            text="AIDIL UTILITY",
            font=("Segoe UI", 16, "bold"),
            bg="#1f1f1f",
            fg="white"
        )

        title.pack(
            pady=(30, 35)
        )

        self.add_button("Dashboard")

        separator = tk.Frame(
            self,
            height=1,
            bg="#3a3a3a"
        )

        separator.pack(
            fill="x",
            padx=20,
            pady=15
        )

        tools = [
            "Productivity",
            "PC Monitor",
            "File Tools",
            "Calculators",
            "Utilities",
            "Network",
            "Media"
        ]

        for tool in tools:
            self.add_button(tool)

        separator2 = tk.Frame(
            self,
            height=1,
            bg="#3a3a3a"
        )

        separator2.pack(
            fill="x",
            padx=20,
            pady=15
        )

        self.add_button("Settings")
        self.add_button("About")

    def add_button(self, name):

        button = tk.Button(
            self,
            text=name,
            anchor="w",
            command=lambda: self.on_page_change(name),
            bg="#1f1f1f",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=25,
            pady=9,
            font=("Segoe UI", 10)
        )

        button.pack(
            fill="x"
        )