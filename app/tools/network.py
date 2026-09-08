import socket
import tkinter as tk


class NetworkTool:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        tk.Label(self.frame, text="Network Tools", font=("Segoe UI", 18, "bold"), bg="white").pack(anchor="w", padx=20, pady=(20, 5))
        row = tk.Frame(self.frame, bg="white")
        row.pack(fill="x", padx=20, pady=15)
        self.host = tk.Entry(row, font=("Segoe UI", 11))
        self.host.insert(0, "example.com")
        self.host.pack(side="left", fill="x", expand=True)
        tk.Button(row, text="Resolve", command=self.resolve).pack(side="left", padx=8)
        self.result = tk.Label(self.frame, text="", bg="white", fg="#666", justify="left")
        self.result.pack(anchor="w", padx=20)

    def resolve(self):
        host = self.host.get().strip()
        try:
            address = socket.gethostbyname(host)
            self.result.config(text=f"Host: {host}\nIP: {address}")
        except socket.gaierror as error:
            self.result.config(text=f"Could not resolve host.\n{error}")
