// Snipsearch AI - JavaScript Code (Using Google Search API)

// URL of the external JSON file (Replace with your own URL)
const jsonURL = "https://raw.githubusercontent.com/KeshavSharma55/Snipsearch_AI.com/refs/heads/main/questions.json";

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

    // Fetch Data from Google Search (By Default)
    response = await fetchGoogleSearch(query);

    return response || "I'm not sure, but I'm still learning!";
}

// Function to evaluate math expressions
function evaluateMath(expression) {
    return Function('"use strict"; return (' + expression + ')')();
}

// Google Search API Fetch (Returning Long Description)
async function fetchGoogleSearch(query) {
    try {
        const apiKey = "AIzaSyDFliUSc0-bUmwbM1YR4wmQXk5wVgGV6-A";  // Your API Key
        const cx = "c7621a78e53794892";                            // Your Search Engine ID
        
        let url = `https://www.googleapis.com/customsearch/v1?q=${encodeURIComponent(query)}&key=${apiKey}&cx=${cx}`;
        let res = await fetch(url);
        let data = await res.json();

        if (data.items && data.items.length > 0) {
            let results = data.items.map(item => 
                `Title: ${item.title}\nDescription: ${item.snippet}\nLink: ${item.link}\n\n`
            ).join('');
            
            return results;
        } else {
            return "No relevant information found.";
        }
    } catch (error) {
        return "Unable to fetch data from Google.";
    }
}
