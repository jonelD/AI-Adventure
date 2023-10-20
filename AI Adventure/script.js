// Get references to HTML elements
const startButton = document.getElementById('startButton');
const output = document.getElementById('output');
const userInput = document.getElementById('userInput');
const replyButton = document.getElementById('replyButton');

// Initialize the SpeechRecognition API
const recognition = new webkitSpeechRecognition(); // For WebKit-based browsers

// Configure recognition options
recognition.continuous = false; // Single speech recognition
recognition.interimResults = false; // Do not return interim results

// Disable user input initially
userInput.disabled = true;
replyButton.disabled = true;

// Event handler for the "Start Adventure" button
startButton.addEventListener('click', () => {
    startButton.disabled = true;
    output.textContent = 'AI: Welcome to the adventure game...';
    setTimeout(() => {
        startButton.style.display = 'none';
        output.style.display = 'block';
        userInput.style.display = 'block';
        replyButton.style.display = 'block';
        userInput.disabled = false;
        replyButton.disabled = false;
    }, 2000);
});

// Event handler for the "Reply" button
replyButton.addEventListener('click', () => {
    const userResponse = userInput.value;
    output.textContent = `User: ${userResponse}`;
    userInput.value = '';

    // Use user's spoken response as human_input
    const response = llm_chain.predict(human_input=userResponse);

    // Convert AI response to speech (text-to-speech)
    const synth = window.speechSynthesis;
    const aiResponse = new SpeechSynthesisUtterance(response);
    synth.speak(aiResponse);

    if (response.includes('The End.')) {
        startButton.style.display = 'block';
        output.style.display = 'none';
        userInput.style.display = 'none';
        replyButton.style.display = 'none';
        startButton.disabled = false;
    }
});