import tkinter as tk


class TextTools:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.input = tk.Text(self.frame, height=8, font=("Consolas", 10), wrap="word")
        self.input.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        self.output = tk.StringVar(value="Characters: 0 | Words: 0 | Lines: 0")
        tk.Label(self.frame, textvariable=self.output, bg="white", fg="#666", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=(0, 10))
        buttons = tk.Frame(self.frame, bg="white")
        buttons.pack(fill="x", padx=20, pady=(0, 20))
        tk.Button(buttons, text="Analyze", command=self.analyze).pack(side="left", padx=(0, 5))
        tk.Button(buttons, text="Uppercase", command=lambda: self.transform(str.upper)).pack(side="left", padx=5)
        tk.Button(buttons, text="Lowercase", command=lambda: self.transform(str.lower)).pack(side="left", padx=5)
        tk.Button(buttons, text="Clear", command=lambda: self.input.delete("1.0", "end")).pack(side="right")

    def analyze(self):
        text = self.input.get("1.0", "end-1c")
        self.output.set(f"Characters: {len(text)} | Words: {len(text.split())} | Lines: {len(text.splitlines())}")

    def transform(self, function):
        text = self.input.get("1.0", "end-1c")
        self.input.delete("1.0", "end")
        self.input.insert("1.0", function(text))
