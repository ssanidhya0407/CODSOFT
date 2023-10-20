import tkinter as tk
from math import sqrt


class CreativeCalculatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")

        self.result_var = tk.StringVar()
        self.result_var.set("0")

        # Entry widget to display the result
        entry = tk.Entry(master, textvariable=self.result_var, font=('Arial', 20), bd=10, insertwidth=4, width=14,
                         justify='right', bg='#F0F0F0')
        entry.grid(row=0, column=0, columnspan=6)

        # Define buttons
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('(', 5, 0), (')', 5, 1), ('√', 5, 2), ('^', 5, 3)
        ]

        # Create buttons
        for (text, row, col) in buttons:
            button = tk.Button(master, text=text, padx=20, pady=20, font=('Arial', 18, 'bold'),
                               command=lambda t=text: self.on_button_click(t), bg='#FFD700', relief='flat')
            button.grid(row=row, column=col, sticky='nsew')
            button.grid_columnconfigure(0, weight=1)
            button.grid_rowconfigure(0, weight=1)

        # Configure column and row weights
        for i in range(6):
            self.master.grid_columnconfigure(i, weight=1)
            self.master.grid_rowconfigure(i, weight=1)

    def on_button_click(self, button_text):
        current_text = self.result_var.get()

        if button_text == 'C':
            self.result_var.set("0")
        elif button_text == '=':
            try:
                result = eval(current_text)
                self.result_var.set(str(result))
            except Exception as e:
                self.result_var.set("Error")
        elif button_text == '√':
            try:
                result = sqrt(float(current_text))
                self.result_var.set(str(result))
            except ValueError:
                self.result_var.set("Error")
        else:
            if current_text == '0' or current_text == 'Error':
                self.result_var.set(button_text)
            else:
                self.result_var.set(current_text + button_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = CreativeCalculatorApp(root)
    root.mainloop()
