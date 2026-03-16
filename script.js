const input = document.getElementById("userInput");
const chatBox = document.getElementById("chatBox");

// Send message on ENTER
input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") sendMessage();
});

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    chatBox.innerHTML += `<p><b>You:</b> ${message}</p>`;
    chatBox.innerHTML += `<p id="thinking"><b>Agent:</b> Thinking...</p>`;
    chatBox.scrollTop = chatBox.scrollHeight;
    input.value = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        document.getElementById("thinking").remove();
        chatBox.innerHTML += `<p><b>Agent:</b> ${data.response}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {
        console.error("Frontend Error:", error);
        document.getElementById("thinking").remove();
        chatBox.innerHTML += `<p><b>Agent:</b> Error connecting to backend.</p>`;
    }
}