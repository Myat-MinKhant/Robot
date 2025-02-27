import re

def simple_maths(command):
    # Extracting numbers and operator from the command
    match = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', command)
    num1, operator, num2 = match.groups()

    # Performing the calculation
    result = None
    if operator == '+':
        result = int(num1) + int(num2)
    elif operator == '-':
        result = int(num1) - int(num2)
    elif operator == '*':
        result = int(num1) * int(num2)
    elif operator == '/':
        result = int(num1) / int(num2)

    return f"The result is {result}"