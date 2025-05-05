import { useEffect, useState } from "react";
import API from "../api";

export default function Chat() {
  const [message, setMessage] = useState("");
  const [history, setHistory] = useState([]);

  const fetchHistory = async () => {
    const res = await API.get("/api/history");
    setHistory(res.data.reverse());
  };

  const sendMessage = async () => {
    if (!message.trim()) return;
    const res = await API.post("/api/chat", { message });
    setHistory((prev) => [...prev, { message, reply: res.data.reply }]);
    speak(res.data.reply);
    setMessage("");
  };

  const speak = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utterance);
  };

  const startVoice = () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.start();
    recognition.onresult = (event) => {
      const spoken = event.results[0][0].transcript;
      setMessage(spoken);
      sendMessage();
    };
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="max-w-xl mx-auto mt-10 space-y-4">
      <h1 className="text-2xl font-bold text-center">GPT Chatbot</h1>
      <div className="h-96 overflow-y-auto border p-4 rounded bg-gray-50">
        {history.map((chat, idx) => (
          <div key={idx} className="mb-4">
            <div><strong>You:</strong> {chat.message}</div>
            <div><strong>Bot:</strong> {chat.reply}</div>
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          className="flex-1 border p-2 rounded"
          placeholder="Type your message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button onClick={sendMessage} className="bg-blue-500 text-white px-4 py-2 rounded">Send</button>
        <button onClick={startVoice} className="bg-gray-300 px-3 rounded">🎤</button>
      </div>
    </div>
  );
}
