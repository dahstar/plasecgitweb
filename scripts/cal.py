# scripts/cal.py

import sys

def cal(a, b, op):
    if op == "sum":
        return a + b
    elif op == "sub":
        return a - b
    elif op == "mul":
        return a * b
    elif op == "div":
        return a / b
    else:
        return "Invalid operation"

if __name__ == "__main__":
    # Get command-line arguments
    if len(sys.argv) != 4:
        print("Usage: cal.py <num1> <num2> <operation>")
        sys.exit(1)

    try:
        num1 = int(sys.argv[1])
        num2 = int(sys.argv[2])
        operation = sys.argv[3]
        result = cal(num1, num2, operation)
        print(result)
    except ValueError:
        print("Invalid input: please provide two numbers.")
