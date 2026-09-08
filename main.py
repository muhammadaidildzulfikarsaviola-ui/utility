import tkinter as tk

from app.ui.window import UtilityApp


def main():
    root = tk.Tk()
    app = UtilityApp(root)
    app.run()


if __name__ == "__main__":
    main()
