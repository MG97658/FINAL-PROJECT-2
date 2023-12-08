# calculator_functions.py
import re
from math import sqrt

class ExpressionEvaluator:
    @staticmethod
    def evaluate_expression(expression: str) -> str:
        try:
            expression = expression.replace('^', '**')
            
            while '(' in expression or ')' in expression:
                match = re.search(r'\(([^()]+)\)', expression)
                if match:
                    subexpression = match.group(1)
                    result = str(eval(subexpression))
                    expression = expression.replace(match.group(0), result)
                else:
                    raise ValueError("Invalid expression: Unmatched parentheses")

            result = str(eval(expression))
            return result
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {e}")
