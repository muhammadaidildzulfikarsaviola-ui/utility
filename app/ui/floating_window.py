import tkinter as tk


class FloatingWindow(tk.Toplevel):

    def __init__(self, parent, title, on_close):

        super().__init__(parent)

        self.on_close = on_close

        self.title(title)

        self.geometry("400x300")

        self.minsize(
            300,
            200
        )

        self.configure(
            bg="white"
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        self.content = tk.Frame(
            self,
            bg="white"
        )

        self.content.pack(
            fill="both",
            expand=True
        )

        self.attributes(
            "-topmost",
            False
        )

    def close(self):

        self.on_close()

        self.destroy()