import re
import math
from textblob import TextBlob

class SmartCalculator:
    def __init__(self):
        self.operations = {
            'plus': '+',
            'minus': '-',
            'times': '*',
            'divided by': '/',
            'sqrt': 'sqrt',
            'power': '**'
        }

    def parse_expression(self, expression):
        for word, symbol in self.operations.items():
            expression = expression.replace(word, symbol)
        
        # Handle power and square root operations
        expression = re.sub(r'sqrt\((.*?)\)', r'math.sqrt(\1)', expression)
        expression = re.sub(r'(\d+)\s*\^\s*(\d+)', r'(\1**\2)', expression)
        
        return expression

    def evaluate_expression(self, expression):
        try:
            # Evaluate the expression
            result = eval(expression, {"__builtins__": None}, {"math": math})
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    def process_request(self, request):
        # Convert the request to lowercase and parse
        request = request.lower()
        expression = self.parse_expression(request)
        result = self.evaluate_expression(expression)
        return result

if __name__ == "__main__":
    calc = SmartCalculator()
    print("Welcome to Smart Calculator!")
    print("Ask me to solve mathematical problems in natural language.")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("Enter your query: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = calc.process_request(user_input)
        print(f"Result: {response}")
