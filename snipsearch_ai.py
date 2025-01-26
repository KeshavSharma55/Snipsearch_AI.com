import math

# Responses for Snipsearch AI
responses = {
    "hello": "Hi there! How can I assist you?",
    "help": "You can ask me to calculate math problems like '2+2', 'sqrt(16)', '3^2', 'sin(30)', 'log(100)', etc.",
    "what is your name": "I'm Snipsearch AI, your assistant.",
    "how are you": "I'm just a bot, but I'm functioning perfectly!",
    "default": "I'm sorry, I don't understand that. Can you try rephrasing?",
    "error": "There was an error processing your input. Please check your syntax.",
}

def get_response(user_input):
    """Get a response based on user input."""
    user_input = user_input.lower().strip()

    # Handle basic commands
    if user_input in responses:
        return responses[user_input]

    # Try to handle math operations
    result = handle_math_operations(user_input)
    if result is not None:
        return f"The result is: {result}"
    
    # If not recognized as math
    return responses["default"]

def handle_math_operations(user_input):
    """Handle advanced math operations."""
    try:
        # Handle square root (sqrt)
        if 'sqrt' in user_input:
            num = float(user_input.replace("sqrt", "").strip("()"))
            return math.sqrt(num)
        
        # Handle exponentiation (x^y)
        if '^' in user_input:
            base, exponent = user_input.split('^')
            return float(base.strip()) ** float(exponent.strip())

        # Trigonometric functions: sin, cos, tan
        if 'sin' in user_input:
            num = float(user_input.replace("sin", "").strip("()"))
            return math.sin(math.radians(num))  # Convert degrees to radians
        
        if 'cos' in user_input:
            num = float(user_input.replace("cos", "").strip("()"))
            return math.cos(math.radians(num))  # Convert degrees to radians
        
        if 'tan' in user_input:
            num = float(user_input.replace("tan", "").strip("()"))
            return math.tan(math.radians(num))  # Convert degrees to radians

        # Logarithmic functions: ln and log
        if 'ln' in user_input:
            num = float(user_input.replace("ln", "").strip("()"))
            return math.log(num)  # Natural log (log base e)
        
        if 'log' in user_input:
            num = float(user_input.replace("log", "").strip("()"))
            return math.log10(num)  # Log base 10

        # Factorial calculation
        if '!' in user_input:
            num = int(user_input.replace("!", "").strip())
            if num < 0:
                return "Error: Factorial of negative numbers is undefined"
            return math.factorial(num)

        # Basic arithmetic (addition, subtraction, multiplication, division)
        allowed_operators = {'+', '-', '*', '/'}
        for operator in allowed_operators:
            if operator in user_input:
                num1, num2 = user_input.split(operator)
                num1 = float(num1.strip())
                num2 = float(num2.strip())

                if operator == '+':
                    return num1 + num2
                elif operator == '-':
                    return num1 - num2
                elif operator == '*':
                    return num1 * num2
                elif operator == '/':
                    if num2 == 0:
                        return "Error: Division by zero"
                    return num1 / num2

    except Exception as e:
        return responses["error"]

    return None  # If no math operation is found


if __name__ == "__main__":
    while True:
        # Read user input
        user_input = input()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! Have a great day!")
            break

        # Get the bot's response
        response = get_response(user_input)
        print(response)