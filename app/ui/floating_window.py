import tkinter as tk


class FloatingWindow(tk.Toplevel):
    def __init__(self, parent, title, on_close, geometry="400x300", always_on_top=False):
        super().__init__(parent)

        self.on_close = on_close
        self.title(title)
        self.geometry(geometry)
        self.minsize(300, 200)
        self.configure(bg="white")

        self.protocol("WM_DELETE_WINDOW", self.close)

        self.content = tk.Frame(self, bg="white")
        self.content.pack(fill="both", expand=True)

        self.toolbar = tk.Frame(self, bg="#f7f7f7", height=34)
        self.toolbar.pack(side="bottom", fill="x")
        self.toolbar.pack_propagate(False)

        self.always_on_top = tk.BooleanVar(value=always_on_top)

        self.top_button = tk.Checkbutton(
            self.toolbar,
            text="Always on top",
            variable=self.always_on_top,
            command=self.toggle_always_on_top,
            bg="#f7f7f7",
            activebackground="#f7f7f7",
            relief="flat",
            bd=0,
            font=("Segoe UI", 9),
        )
        self.top_button.pack(side="right", padx=8)

        self.attributes("-topmost", always_on_top)

    def toggle_always_on_top(self):
        self.attributes("-topmost", self.always_on_top.get())

    def get_geometry(self):
        return self.geometry()

    def close(self):
        self.on_close(self)
        self.destroy()
