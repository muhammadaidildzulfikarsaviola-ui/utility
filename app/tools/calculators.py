import tkinter as tk


class CalculatorsTool:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.expression = tk.StringVar()
        entry = tk.Entry(self.frame, textvariable=self.expression, font=("Segoe UI", 18), justify="right")
        entry.pack(fill="x", padx=20, pady=20)
        entry.bind("<Return>", lambda event: self.calculate())

        buttons = [
            ("7", "8", "9", "/"),
            ("4", "5", "6", "*"),
            ("1", "2", "3", "-"),
            ("0", ".", "C", "+"),
            ("=",),
        ]
        for row in buttons:
            line = tk.Frame(self.frame, bg="white")
            line.pack(fill="x", padx=20)
            for value in row:
                tk.Button(line, text=value, font=("Segoe UI", 12), command=lambda v=value: self.press(v)).pack(side="left", fill="x", expand=True, padx=2, pady=2)

    def press(self, value):
        if value == "=":
            self.calculate()
        elif value == "C":
            self.expression.set("")
        else:
            self.expression.set(self.expression.get() + value)

    def calculate(self):
        expression = self.expression.get().strip()
        if not expression or any(char not in "0123456789.+-*/() " for char in expression):
            self.expression.set("Invalid")
            return
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            self.expression.set(str(result))
        except Exception:
            self.expression.set("Error")
