/* script.js */
const predefinedResponses = {
    "hello": "Hello! How can I assist you today?",
    "how are you": "I'm just a chatbot, but I'm here to help!",
    "what is your name": "I'm Snipsearch AI, your virtual assistant.",
    "bye": "Goodbye! Have a great day!"
};

async function fetchFromGeminiAPI(userInput) {
    // Replace 'YOUR_GEMINI_API_KEY' with your actual API key
    const response = await fetch(`https://api.gemini.com/v1/query?text=${encodeURIComponent(userInput)}&key=AIzaSyDXh8VUYY4TffToiulBhBSG6JZpOnzJ7hM`);
    const data = await response.json();
    return data.response || "I'm not sure, but I can learn!";
}

function sendMessage() {
    const userInput = document.getElementById("user-input").value.toLowerCase();
    const chatMessages = document.getElementById("chat-messages");
    
    if (!userInput) return;
    
    // Add user message to chat
    chatMessages.innerHTML += `<div><strong>You:</strong> ${userInput}</div>`;
    document.getElementById("user-input").value = "";
    
    setTimeout(async () => {
        let botResponse = predefinedResponses[userInput] || await fetchFromGeminiAPI(userInput);
        chatMessages.innerHTML += `<div><strong>Snipsearch AI:</strong> ${botResponse}</div>`;
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 1000);
}
