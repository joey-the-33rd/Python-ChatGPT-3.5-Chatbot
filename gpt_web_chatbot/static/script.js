const chat = document.getElementById("chat");
const messageInput = document.getElementById("message");

function appendMessage(sender, text) {
  chat.innerHTML += `${sender}: ${text}\n`;
  chat.scrollTop = chat.scrollHeight;
}

function sendMessage() {
  const message = messageInput.value.trim();
  if (!message) return;

  appendMessage("You", message);
  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  })
    .then(res => res.json())
    .then(data => {
      appendMessage("Bot", data.reply);
      speak(data.reply);
    });

  messageInput.value = "";
}

function speak(text) {
  const utter = new SpeechSynthesisUtterance(text);
  speechSynthesis.speak(utter);
}

function startVoice() {
  const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.start();

  recognition.onresult = function(event) {
    const voiceText = event.results[0][0].transcript;
    messageInput.value = voiceText;
    sendMessage();
  };
}
