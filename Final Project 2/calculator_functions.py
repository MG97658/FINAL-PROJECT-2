# calculator_functions.py
import re
from math import sqrt

class ExpressionEvaluator:
    @staticmethod
    def evaluate_expression(expression: str) -> str:
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
            # Replace '^' with '**' for exponentiation
            expression = expression.replace('^', '**')
            
            # Evaluate expressions within parentheses
            while '(' in expression or ')' in expression:
                match = re.search(r'\(([^()]+)\)', expression)
                if match:
                    subexpression = match.group(1)
                    result = str(eval(subexpression))
                    expression = expression.replace(match.group(0), result)
                else:
                    raise ValueError("Invalid expression: Unmatched parentheses")

            # Evaluate the final expression
            result = str(eval(expression))
            return result
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {e}")
