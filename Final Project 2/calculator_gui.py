# calculator_gui.py
import os
import tkinter as tk
from calculator_functions import ExpressionEvaluator
import csv
from datetime import datetime
from math import sqrt  # Import sqrt for square root calculation

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Calculator")

        self.result_var = tk.StringVar()
        self.result_var.set("0")

        self.create_widgets()

    def create_widgets(self):
        entry = tk.Entry(self.master, textvariable=self.result_var, font=('Helvetica', 14), bd=10, relief='ridge', justify='right')
        entry.grid(row=0, column=0, columnspan=4)
        entry.bind('<Return>', self.on_return_key_pressed)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            '(', ')', '^', 'C',
            '√',  # Add a new button for square root
            'A',  # Add a new button for square area
        ]

        row, col = 1, 0
        for button_text in buttons:
            button = tk.Button(self.master, text=button_text, padx=20, pady=20, font=('Helvetica', 12),
                               command=lambda value=button_text: self.on_button_click(value))
            button.grid(row=row, column=col, sticky='nsew', ipadx=5, ipady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1

        for r in range(1, 6):
            self.master.grid_rowconfigure(r, weight=1)
        for c in range(4):
            self.master.grid_columnconfigure(c, weight=1)

    def on_return_key_pressed(self, event):
        self.on_button_click('=')

    def evaluate_expression(self, expression):
        try:
            result = ExpressionEvaluator.evaluate_expression(expression)
            self.save_calculation(expression, result)
            return result
        except ValueError as ve:
            print(ve)
            return "Error"

    def on_button_click(self, value):
        current_text = self.result_var.get()

        if value == '=':
            result = self.evaluate_expression(current_text)
            self.result_var.set(result)
        elif value == 'C':
            self.result_var.set("0")
        elif value == '√':
            # Calculate square root
            try:
                result = str(sqrt(float(current_text)))
                self.result_var.set(result)
                self.save_calculation(f'sqrt({current_text})', result)
            except ValueError as ve:
                print(ve)
                self.result_var.set("Error")
        elif value == 'A':
            # Calculate square area
            try:
                side_length = float(current_text)
                area = side_length ** 2
                result = str(area)
                self.result_var.set(result)
                self.save_calculation(f'Area of square with side length {side_length}', result)
            except ValueError as ve:
                print(ve)
                self.result_var.set("Error")

        else:
            if current_text == '0' and value.isdigit():
                self.result_var.set(value)
            else:
                self.result_var.set(current_text + value)

    def save_calculation(self, expression, result):
        # Get the user's home directory
        home_dir = os.path.expanduser("~")
        file_path = os.path.join(home_dir, 'calculation_history.csv')

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(file_path, 'a', newline='') as csvfile:
            fieldnames = ['Timestamp', 'Expression', 'Result']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # If the file is empty, write the header
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow({'Timestamp': timestamp, 'Expression': expression, 'Result': result})

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
