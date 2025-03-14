// Snipsearch AI - JavaScript Code (Fixed URL Fetch Method)

// URL of the external JSON file (Replace with your own URL)
const jsonURL = "https://raw.githubusercontent.com/YourUsername/YourRepository/main/questions.json";

// Variable to store predefined responses
let predefinedResponses = {};

// Load predefined questions from JSON file
async function loadPredefinedQuestions() {
    try {
        const response = await fetch(jsonURL, {cache: "no-cache"});
        if (!response.ok) {
            throw new Error("Network response was not ok.");
        }
        predefinedResponses = await response.json();
        console.log("Predefined questions loaded successfully.", predefinedResponses);
    } catch (error) {
        console.error("Error loading predefined questions:", error);
    }
}

// Call the function to load questions
loadPredefinedQuestions();

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

    // Fetch Data from DuckDuckGo (By Default)
    response = await fetchDuckDuckGo(query);

    return response || "I'm not sure, but I'm still learning!";
}

// Function to evaluate math expressions
function evaluateMath(expression) {
    return Function('"use strict"; return (' + expression + ')')();
}

// DuckDuckGo API Search
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
