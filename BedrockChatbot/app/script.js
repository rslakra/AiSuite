document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chatbot-messages');

    function appendMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(`${sender}-message`);
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to latest message
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        appendMessage('user', message);
        userInput.value = ''; // Clear input field

        // In a real application, you'd send 'message' to your backend
        // (e.g., using fetch or Axios) and get a response.
        // For this example, we'll simulate a bot response.
        
        // Example with a simulated response:
        setTimeout(() => {
            const botResponse = `I received your message: "${message}". How else can I help?`;
            appendMessage('bot', botResponse);
        }, 500);

        // Example if you were to integrate with a backend:
        /*
        try {
            const response = await fetch('/api/chat', { // Your backend API endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });
            const data = await response.json();
            appendMessage('bot', data.botResponse);
        } catch (error) {
            console.error('Error sending message:', error);
            appendMessage('bot', 'Sorry, something went wrong. Please try again.');
        }
        */
    }

    sendButton.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Initial bot greeting
    appendMessage('bot', 'Hello! How can I assist you today?');
});
