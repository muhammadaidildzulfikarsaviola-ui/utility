import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, parent, on_page_change):
        super().__init__(parent, width=220, bg="#1f1f1f")
        self.on_page_change = on_page_change
        self.pack_propagate(False)

        tk.Label(self, text="AIDIL UTILITY", font=("Segoe UI", 16, "bold"), bg="#1f1f1f", fg="white").pack(pady=(30, 30))
        self.add_button("Dashboard")
        self.separator()

        for tool in [
            "Productivity", "PC Monitor", "File Tools", "Calculators",
            "Utilities", "Windows Tools", "Network", "Media"
        ]:
            self.add_button(tool)

        self.separator()
        self.add_button("Settings")
        self.add_button("About")

    def separator(self):
        tk.Frame(self, height=1, bg="#3a3a3a").pack(fill="x", padx=20, pady=12)

    def add_button(self, name):
        tk.Button(
            self, text=name, anchor="w",
            command=lambda n=name: self.on_page_change(n),
            bg="#1f1f1f", fg="white",
            activebackground="#333333", activeforeground="white",
            relief="flat", bd=0, padx=25, pady=9,
            font=("Segoe UI", 10)
        ).pack(fill="x")
