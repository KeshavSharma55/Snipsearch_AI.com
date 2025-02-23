import tkinter as tk
from tkinter import scrolledtext
import math
import time

# Database for predefined Q&A, jokes, facts
database = {
    "jokes": [
        "Why don’t skeletons fight each other? They don’t have the guts!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!"
    ],
    "facts": [
        "Did you know? Honey never spoils!",
        "A day on Venus is longer than a year on Venus.",
        "Octopuses have three hearts!"
    ],
    "qa": {
        "who created you": "I was created by Copenet Technologies.",
        "what is your name": "I am Snipsearch AI, your smart assistant.",
        "tell me a joke": lambda: database["jokes"][0],
        "tell me a fact": lambda: database["facts"][0]
    }
}

# Function to show splash screen
def show_splash():
    splash = tk.Toplevel()
    splash.geometry("300x200")
    splash.title("Snipsearch AI")
    splash.configure(bg="black")

    label = tk.Label(splash, text="Snipsearch AI", font=("Arial", 20, "bold"), fg="white", bg="black")
    label.pack(expand=True)

    splash.update()
    time.sleep(3)  # Show splash for 3 seconds
    splash.destroy()
    root.deiconify()  # Show main app

# Function to handle chat response
def get_response(user_input):
    user_input = user_input.lower().strip()

    if user_input in database["qa"]:
        return database["qa"][user_input]() if callable(database["qa"][user_input]) else database["qa"][user_input]

    try:
        return str(eval_math(user_input))
    except:
        return "I'm still learning! Try asking about jokes, facts, or enter a math calculation."

# Function to evaluate math expressions
def eval_math(expression):
    expression = expression.replace("^", "**")  
    expression = expression.replace("sqrt(", "math.sqrt(")  
    return eval(expression, {"math": math, "__builtins__": {}})  

# Function to update chat UI
def send_message():
    user_text = user_input.get().strip()
    if user_text == "":
        return

    chat_box.insert(tk.END, f"You: {user_text}\n", "user")
    response = get_response(user_text)
    chat_box.insert(tk.END, f"AI: {response}\n\n", "bot")

    user_input.delete(0, tk.END)
    chat_box.yview(tk.END)

# Toggle dark mode
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode

    bg_color = "#1a1a1a" if dark_mode else "white"
    text_color = "white" if dark_mode else "black"

    root.configure(bg=bg_color)
    chat_box.configure(bg=bg_color, fg=text_color)
    user_input.configure(bg=bg_color, fg=text_color)
    send_button.configure(bg="#007bff" if dark_mode else "#007bff", fg="white")

# Initialize main window (hidden initially)
root = tk.Tk()
root.title("Snipsearch AI")
root.geometry("400x500")
root.configure(bg="white")
root.withdraw()  # Hide window during splash screen

# Show splash screen before opening main app
root.after(100, show_splash)

# Chat Display
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=20, bg="white", fg="black", font=("Arial", 12))
chat_box.pack(padx=10, pady=10)
chat_box.insert(tk.END, "AI: Welcome to Snipsearch AI - Index Model\n\n", "bot")
chat_box.insert(tk.END, "AI: This AI supports advanced math calculations, jokes, facts, and Q&A!\n\n", "bot")

# Text Input
user_input = tk.Entry(root, width=40, font=("Arial", 12))
user_input.pack(pady=5)

# Send Button
send_button = tk.Button(root, text="Send", command=send_message, bg="#007bff", fg="white", font=("Arial", 12))
send_button.pack(pady=5)

# Dark Mode Toggle Button
dark_mode = False
toggle_button = tk.Button(root, text="Dark Mode", command=toggle_dark_mode, font=("Arial", 10))
toggle_button.pack(pady=5)

# Custom Styles
chat_box.tag_config("user", foreground="blue", font=("Arial", 12, "bold"))
chat_box.tag_config("bot", foreground="green", font=("Arial", 12, "italic"))

root.mainloop()