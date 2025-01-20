async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const message = inputField.value.trim();

    // Prevent empty messages
    if (message === "") {
        return;
    }

    // Append the user's message to the chat box
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'message user';
    userMessageDiv.textContent = message;
    chatBox.appendChild(userMessageDiv);

    // Clear the input field
    inputField.value = "";

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // Send the user's message to the Flask backend
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        // Append the bot's reply to the chat box
        const botMessageDiv = document.createElement('div');
        botMessageDiv.className = 'message bot';
        botMessageDiv.textContent = data.reply;
        chatBox.appendChild(botMessageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        console.error('Error sending message:', error);
        const errorMessageDiv = document.createElement('div');
        errorMessageDiv.className = 'message bot';
        errorMessageDiv.textContent = "Oops! Something went wrong. Please try again later.";
        chatBox.appendChild(errorMessageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}
