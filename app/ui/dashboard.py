import tkinter as tk


class Dashboard(tk.Frame):

    def __init__(self, parent):

        super().__init__(
            parent,
            bg="#f2f2f2"
        )

        title = tk.Label(
            self,
            text="Dashboard",
            font=("Segoe UI", 26, "bold"),
            bg="#f2f2f2",
            fg="#202020"
        )

        title.pack(
            anchor="w",
            padx=40,
            pady=(35, 5)
        )

        subtitle = tk.Label(
            self,
            text="Your laptop activity at a glance.",
            font=("Segoe UI", 11),
            bg="#f2f2f2",
            fg="#666666"
        )

        subtitle.pack(
            anchor="w",
            padx=40,
            pady=(0, 30)
        )

        self.create_card(
            "Laptop Usage",
            "0h 00m",
            "Today's active time"
        )

        self.create_card(
            "Applications",
            "0",
            "Applications tracked"
        )

        self.create_card(
            "Most Used",
            "None",
            "Most active application"
        )

    def create_card(self, title, value, description):

        card = tk.Frame(
            self,
            bg="white",
            height=110
        )

        card.pack(
            fill="x",
            padx=40,
            pady=6
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 10),
            bg="white",
            fg="#777777"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 0)
        )

        tk.Label(
            card,
            text=value,
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#202020"
        ).pack(
            anchor="w",
            padx=20
        )

        tk.Label(
            card,
            text=description,
            font=("Segoe UI", 9),
            bg="white",
            fg="#999999"
        ).pack(
            anchor="w",
            padx=20
        )