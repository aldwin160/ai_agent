def calculate(expression):
    parts = expression.split()
    if len(parts) < 3:
        return 'Invalid Expression'

    #Evaluate multiplication first
    def evaluate_multiplication(expression_parts):
        new_parts = []
        i = 0
        while i < len(expression_parts):
            if expression_parts[i] == '*':
                result = int(new_parts[-1]) * int(expression_parts[i+1])
                new_parts[-1] = str(result)
                i += 2
            else:
                new_parts.append(expression_parts[i])
                i += 1
        return new_parts

    parts = evaluate_multiplication(parts)

    #Evaluate addition
    result = int(parts[0])
    i = 1
    while i < len(parts) - 1:
        operator = parts[i]
        operand = int(parts[i+1])
        if operator == '+':
            result += operand
        else:
            return 'Invalid Operator'
        i += 2
    return result

expression = '3 + 7 * 2'
print(calculate(expression))