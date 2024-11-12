# mychatapp/scripts/cal.py

def cal(a, b, op):
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return "Invalid numbers provided."

    if op == "sum":
        return a + b
    elif op == "sub":
        return a - b
    elif op == "mul":
        return a * b
    elif op == "div":
        if b == 0:
            return "Division by zero is not allowed."
        return a / b
    else:
        return "Invalid operation. Use 'sum', 'sub', 'mul', or 'div'."
