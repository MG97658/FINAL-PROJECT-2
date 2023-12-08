# calculator_gui.py
import os
import tkinter as tk
from calculator_functions import ExpressionEvaluator
import csv
from datetime import datetime
from math import sqrt  # Import sqrt for square root calculation

class CalculatorApp:
    def __init__(self, master: tk.Tk):
        """
        Initializes the CalculatorApp.

        Args:
            master (tk.Tk): The root window of the application.
        """
        self.master = master
        self.master.title("Advanced Calculator")

        self.result_var = tk.StringVar()
        self.result_var.set("0")

        self.create_widgets()

    def create_widgets(self):
        """
        Creates and configures the widgets for the calculator GUI.
        """
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

    def on_return_key_pressed(self, event: tk.Event):
        """
        Event handler for the 'Return' key press event.

        Args:
            event (tk.Event): The event object.
        """
        self.on_button_click('=')

    def evaluate_expression(self, expression: str) -> str:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The mathematical expression to be evaluated.

        Returns:
            str: The result of the evaluated expression as a string.

        Raises:
            ValueError: If the expression contains unmatched parentheses or encounters an evaluation error.
        """
        try:
            result = ExpressionEvaluator.evaluate_expression(expression)
            self.save_calculation(expression, result)
            return result
        except ValueError as ve:
            print(ve)
            return "Error"

    def on_button_click(self, value: str):
        """
        Event handler for button clicks.

        Args:
            value (str): The value associated with the clicked button.
        """
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
        elif value == '(':
            # Handle the case when '(' is added after '0'
            if current_text == '0':
                self.result_var.set(value)
            else:
                self.result_var.set(current_text + value)
        else:
            if current_text == '0' and value.isdigit():
                self.result_var.set(value)
            else:
                self.result_var.set(current_text + value)

    def save_calculation(self, expression: str, result: str):
        """
        Saves a calculation to a CSV file.

        Args:
            expression (str): The mathematical expression.
            result (str): The result of the expression.
        """
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
