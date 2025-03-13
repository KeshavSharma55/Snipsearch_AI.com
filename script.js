// Snipsearch AI - JavaScript Code (DuckDuckGo Enhanced Version)

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

// Predefined responses
const predefinedResponses = {
    "hello": "Hi! How can I assist you today?",
    "how are you?": "I'm just a bot, but I'm doing great!",
    "who created you?": "I was created by Copenet Technologies.",
    "what is ai?": "AI stands for Artificial Intelligence, which enables machines to mimic human intelligence."
};

// Function to process user query
async function getBotResponse(query) {
    let response = "";

    // Check for predefined responses
    if (predefinedResponses[query.toLowerCase()]) {
        return predefinedResponses[query.toLowerCase()];
    }

    // Check for math calculations
    if (query.match(/[\d+\-*/()]/)) {
        try {
            return "Result: " + evaluateMath(query);
        } catch (error) {
            return "Invalid math expression.";
        }
    }

    // Fetch Data from DuckDuckGo (By Default)
    response = await fetchDuckDuckGo(query);

    return response || "I'm not sure, but I'm still learning!";
}

// Function to evaluate math expressions
function evaluateMath(expression) {
    return Function('"use strict"; return (' + expression + ')')();
}

// DuckDuckGo API Search (For Everything)
async function fetchDuckDuckGo(query) {
    try {
        let url = `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json`;
        let res = await fetch(url);
        let data = await res.json();
        
        if (data.Abstract) {
            return data.Abstract;
        } else if (data.RelatedTopics && data.RelatedTopics.length > 0) {
            let relatedInfo = data.RelatedTopics[0].Text;
            return relatedInfo ? `DuckDuckGo: ${relatedInfo}` : "No relevant information found.";
        } else {
            return "No relevant information found.";
        }
    } catch (error) {
        return "Unable to fetch data from DuckDuckGo.";
    }
}