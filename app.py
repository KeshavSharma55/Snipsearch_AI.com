import tkinter as tk
from tkinter import scrolledtext
import math
import requests

# 🔹 Replace with your actual Gemini API Key
GEMINI_API_KEY = "AIzaSyAT8zICkBqXtw77X-SdlX1AOkchxypSevY"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# 🔹 Inbuilt Database
database = {
    "qa": {
        "who created you": "I was created by Keshav Sharma.",
        "hello": "Hi, How Can I help you.",
        "what is your name": "I am Snipsearch AI, your smart AI assistant.",
    }
}

# 🔹 Function to Get Response from Gemini API
def get_gemini_response(query):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": query}]}],
        "generationConfig": {"temperature": 0.7}
    }

    try:
        response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", json=data, headers=headers)
        response_json = response.json()
        
        if "candidates" in response_json and response_json["candidates"]:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "I'm not sure, try asking something else!"
    except Exception as e:
        return f"Error: {str(e)}"
        
 


# 🔹 Function to Evaluate Math Expressions
def eval_math(expression):
    expression = expression.replace("^", "**")  
    expression = expression.replace("sqrt(", "math.sqrt(")  
    return eval(expression, {"math": math, "__builtins__": {}})

# 🔹 Function to Handle User Input
def get_response(user_input):
    user_input = user_input.lower().strip()

    # Check if user input is in predefined database
    if user_input in database["qa"]:
        return database["qa"][user_input]() if callable(database["qa"][user_input]) else database["qa"][user_input]

    # Check if input is a math expression
    try:
        return str(eval_math(user_input))
    except:
        pass

    # If not found, call Gemini AI API
    return get_gemini_response(user_input)

# 🔹 Function to Send Message in Chat UI
def send_message():
    user_text = user_input.get().strip()
    if user_text == "":
        return

    chat_box.insert(tk.END, f"You: {user_text}\n", "user")
    response = get_response(user_text)
    chat_box.insert(tk.END, f"Snipsearch AI: {response}\n\n", "bot")

    user_input.delete(0, tk.END)
    chat_box.yview(tk.END)

# 🔹 Dark Mode Toggle
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode

    bg_color = "#1a1a1a" if dark_mode else "white"
    text_color = "white" if dark_mode else "black"

    root.configure(bg=bg_color)
    chat_box.configure(bg=bg_color, fg=text_color)
    user_input.configure(bg=bg_color, fg=text_color)
    send_button.configure(bg="#007bff" if dark_mode else "#007bff", fg="white")
    


# 🌟 Function to Show Splash Screen
def show_splash():
    splash = tk.Toplevel(root)
    splash.geometry("800x1400")
    splash.configure(bg="black")
    
    label = tk.Label(splash, text="Snipsearch AI", font=("Arial", 24, "bold"), fg="white", bg="black")
    label.pack(expand=True)

    root.withdraw()  # Hide main window
    splash.after(3000, lambda: (splash.destroy(), root.deiconify()))  # 3 sec delay then show main app

# 🌟 Initialize Main Window
root = tk.Tk()
root.title("Snipsearch AI")
root.geometry("400x500")
root.configure(bg="white")

# 🌟 Show Splash Screen Before Main Window
root.after(0, show_splash)

# 🔹 Chat Display Box
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=20, bg="white", fg="black", font=("Arial", 12))
chat_box.pack(padx=10, pady=10)
chat_box.insert(tk.END, "Snipsearch AI: Welcome to Snipsearch AI - Index Model\n\n", "bot")
chat_box.insert(tk.END, "Snipsearch AI: Ask me anything! I support math, jokes, facts, and more.\n\n", "bot")
chat_box.insert(tk.END, "Snipsearch AI: I might be slow so please wait 50 Seconds to get full Result.\n\n", "bot")

# 🔹 Text Input Field
user_input = tk.Entry(root, width=40, font=("Arial", 12))
user_input.pack(pady=5)

# 🔹 Send Button
send_button = tk.Button(root, text="Send", command=send_message, bg="#007bff", fg="white", font=("Arial", 12))
send_button.pack(pady=5)

# 🔹 Dark Mode Toggle Button
dark_mode = False
toggle_button = tk.Button(root, text="Dark Mode", command=toggle_dark_mode, font=("Arial", 10))
toggle_button.pack(pady=5)

#Clear chat
def clear_chat():
    chat_box.delete(1.0, tk.END)

clear_button = tk.Button(root, text="🗑️ Clear Chat", command=clear_chat, font=("Arial", 10))
clear_button.pack(pady=5)

# 🔹 Custom Text Styles
chat_box.tag_config("user", foreground="blue", font=("Arial", 12, "bold"))
chat_box.tag_config("bot", foreground="green", font=("Arial", 12, "italic"))

# 🔹 Run Tkinter Main Loop
root.mainloop()