let chatBox = document.getElementById("chat-box");

// AI database (predefined questions & answers)
let aiDatabase = {
    "hello": "Hi there! How can I help you?",
    "who are you": "I am Snipsearch AI, your intelligent assistant!",
    "what is your name": "My name is Snipsearch AI.",
    "who created you": "I am created by Keshav Sharma, a Programmer and Founder of Snipsearch AI.",
    "how are you": "I'm just a bot, but I'm always here to help!"
};

// Function to display messages
function addMessage(sender, message) {
    chatBox.innerHTML += `<p><strong>${sender}:</strong> ${message}</p>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Math calculation function
function calculateMath(expression) {
    try {
        return eval(expression);
    } catch (error) {
        return "I can't solve that.";
    }
}

// Fetch Wikipedia summary
async function searchWikipedia(query) {
    let url = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(query)}`;
    let response = await fetch(url);
    let data = await response.json();
    return data.extract ? data.extract : "No Wikipedia summary found.";
}

// Fetch Google-like search results using DuckDuckGo
async function searchGoogle(query) {
    let url = `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json`;
    let response = await fetch(url);
    let data = await response.json();

    if (data.RelatedTopics.length > 0) {
        return `🔍 **Top Result:** <a href="${data.RelatedTopics[0].FirstURL}" target="_blank">${data.RelatedTopics[0].Text}</a>`;
    } else {
        return "No search results found.";
    }
}

// Handle user input
async function sendMessage() {
    let userInput = document.getElementById("user-input").value.trim().toLowerCase();
    document.getElementById("user-input").value = "";

    if (userInput === "") return;
    
    addMessage("You", userInput);

    // Check AI database
    if (aiDatabase[userInput]) {
        addMessage("Snipsearch AI", aiDatabase[userInput]);
    } else if (!isNaN(calculateMath(userInput))) {
        addMessage("Snipsearch AI", "Answer: " + calculateMath(userInput));
    } else {
        addMessage("Snipsearch AI", "Searching for information...");

        let wikiResult = await searchWikipedia(userInput);
        let googleResult = await searchGoogle(userInput);

        addMessage("Snipsearch AI", `📖: ${wikiResult}`);
        addMessage("Snipsearch AI", googleResult);

        // Learn new answers from user
        let newAnswer = prompt("I don't know the answer. Can you teach me?");
        if (newAnswer) {
            aiDatabase[userInput] = newAnswer;
            addMessage("Snipsearch AI", "Thanks! I've learned a new answer.");
        }
    }
}

// Handle Enter key press
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}