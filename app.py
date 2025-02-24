from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allows frontend requests

# Predefined Questions & Answers
database = {
    "who created you": "I was created by Keshav Sharma.",
    "what is your name": "I am Snipsearch AI, your smart assistant.",
}

# Gemini API Key (Replace with your actual API Key)
GEMINI_API_KEY = "AIzaSyAT8zICkBqXtw77X-SdlX1AOkchxypSevY"

# Function to call Gemini API
def get_gemini_response(query):
    url = f"https://api.generativeai.google/v1/models/gemini-pro:generateText?key={GEMINI_API_KEY}"
    data = {"prompt": {"text": query}}
    response = requests.post(url, json=data)
    return response.json().get("text", "I couldn't process that.")

# Route for AI chatbot
@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query", "").lower()
    
    # Check predefined responses
    if user_query in database:
        return jsonify({"response": database[user_query]})
    
    # Otherwise, call Gemini API
    return jsonify({"response": get_gemini_response(user_query)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)