// Snipsearch AI - JavaScript Code (Using Google Search API with Predefined Questions)

// Predefined responses stored directly in the script
const predefinedResponses = {
    "what is snipsearch ai?": "Snipsearch AI is an advanced AI chatbot designed to assist you with various queries, calculations, and more!",
    "who created snipsearch ai?": "Snipsearch AI was created by Keshav Sharma under Copenet Technologies.",
    "what is ai?": "AI stands for Artificial Intelligence, which is the simulation of human intelligence in machines that can perform tasks requiring human-like thinking.",
    "hello": "Hello! How can I assist you today?",
    "how are you?": "I'm just a program, but thanks for asking! How can I help you today?"
};

// Function to send user message
async function sendMessage() {
    let inputBox = document.getElementById("user-input");
    let userText = inputBox.value.trim();
    if (userText === "") return;

    addMessage("User", userText);
    inputBox.value = "";

    let response = await getBotResponse(userText);
    addMessage("Snipsearch AI", response);
}

// Function to display messages in chat
function addMessage(sender, text) {
    let chatBox = document.getElementById("chat-box");
    let msgDiv = document.createElement("div");
    msgDiv.innerHTML = `<b>${sender}:</b> ${text}`;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to process user query
async function getBotResponse(query) {
    let response = "";

    // Check for predefined responses (Case-insensitive search)
    const lowerCaseQuery = query.toLowerCase();
    if (predefinedResponses[lowerCaseQuery]) {
        return predefinedResponses[lowerCaseQuery];
    }

    // Check for math calculations
    if (query.match(/[\d+\-*/()]/)) {
        try {
            return "Result: " + evaluateMath(query);
        } catch (error) {
            return "Invalid math expression.";
        }
    }

    // Fetch Data from Google Search (By Default)
    response = await fetchGoogleSearch(query);

    return response || "I'm not sure, but I'm still learning!";
}

// Function to evaluate math expressions
function evaluateMath(expression) {
    return Function('"use strict"; return (' + expression + ')')();
}

// Google Search API Fetch (Returning Clickable Links)
async function fetchGoogleSearch(query) {
    try {
        const apiKey = "AIzaSyDFliUSc0-bUmwbM1YR4wmQXk5wVgGV6-A";  // Your API Key
        const cx = "c7621a78e53794892";                            // Your Search Engine ID
        
        let url = `https://www.googleapis.com/customsearch/v1?q=${encodeURIComponent(query)}&key=${apiKey}&cx=${cx}`;
        let res = await fetch(url);
        let data = await res.json();

        if (data.items && data.items.length > 0) {
            let results = data.items.map(item => 
                `Title: ${item.title}<br>Description: ${item.snippet}<br>Link: <a href="${item.link}" target="_blank">${item.link}</a><br><br>`
            ).join('');
            
            return results;
        } else {
            return "No relevant information found.";
        }
    } catch (error) {
        return "Unable to fetch data from Google.";
    }
}
