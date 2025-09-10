document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatBox = document.getElementById('chat-box');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const micBtn = document.getElementById('mic-btn');

    // Voice Recording Variables
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    // --- Initial Bot Message ---
    // Start the conversation as soon as the page loads
    const startConversation = async () => {
        addTypingIndicator();
        // A small delay to simulate the bot "thinking"
        setTimeout(() => {
            const firstMessage = "Hello! I'm an AI assistant from Innovate Inc. I'm here to ask a few quick questions to qualify your lead. First, what is your name?";
            addMessage(firstMessage, 'bot');
            speak(firstMessage);
            removeTypingIndicator();
        }, 1000);
    };

    // --- UI Helper Functions ---
    const addMessage = (message, sender) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the latest message
    };

    const addTypingIndicator = () => {
        const typingElement = document.createElement('div');
        typingElement.classList.add('message', 'bot', 'typing-indicator');
        typingElement.innerHTML = '<span></span><span></span><span></span>';
        chatBox.appendChild(typingElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    const removeTypingIndicator = () => {
        const indicator = chatBox.querySelector('.typing-indicator');
        if (indicator) {
            chatBox.removeChild(indicator);
        }
    };

    // --- Core Logic ---
    const handleTextInput = async () => {
        const message = chatInput.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        chatInput.value = '';
        addTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message }),
            });

            if (!response.ok) throw new Error('Network response was not ok.');

            const data = await response.json();
            removeTypingIndicator();
            addMessage(data.response, 'bot');
            speak(data.response); // Text-to-speech for the bot's response
        } catch (error) {
            console.error('Error during chat:', error);
            removeTypingIndicator();
            addMessage("I'm having trouble connecting. Please try again.", 'bot');
        }
    };
    
    // --- Voice Input Logic ---
    const handleMicInput = async () => {
        if (!isRecording) {
            // Start Recording
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();

                isRecording = true;
                micBtn.classList.add('recording');
                audioChunks = []; // Clear previous recording chunks

                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });

                mediaRecorder.addEventListener('stop', sendAudioToServer);

            } catch (error) {
                console.error('Error accessing microphone:', error);
                alert('Microphone access was denied. Please allow access to use this feature.');
            }
        } else {
            // Stop Recording
            mediaRecorder.stop();
            isRecording = false;
            micBtn.classList.remove('recording');
        }
    };

    const sendAudioToServer = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('audio_data', audioBlob);

        addTypingIndicator();

        try {
            const response = await fetch('/voice', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Network response was not ok.');

            const data = await response.json();
            removeTypingIndicator();

            // Display the transcribed user message and the bot's response
            if (data.user_message) addMessage(data.user_message, 'user');
            if (data.response) addMessage(data.response, 'bot');
            
            // Play the bot's audio response
            if (data.audio_url) {
                const audio = new Audio(data.audio_url);
                audio.play();
            }

        } catch (error) {
            console.error('Error sending audio:', error);
            removeTypingIndicator();
            addMessage("Sorry, I couldn't process the audio. Please try again.", 'bot');
        }
    };
    
    // --- Text-to-Speech Function ---
    const speak = (text) => {
        // Basic TTS using the browser's built-in capabilities as a fallback
        // The primary TTS is handled by the backend for voice interactions
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            window.speechSynthesis.speak(utterance);
        }
    };

    // --- Event Listeners ---
    sendBtn.addEventListener('click', handleTextInput);
    chatInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            handleTextInput();
        }
    });
    micBtn.addEventListener('click', handleMicInput);

    // --- Initialization ---
    startConversation();
});
