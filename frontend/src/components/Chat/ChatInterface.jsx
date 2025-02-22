import { useState } from "react";
import { PaperAirplaneIcon } from "@heroicons/react/24/outline";

export default function ChatInterface() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      content: "Hello! I'm your tax assistant. How can I help you today?",
      timestamp: new Date(),
    },
  ]);
  const [inputMessage, setInputMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      type: "user",
      content: inputMessage.trim(),
      timestamp: new Date(),
    };

    // Add bot response (placeholder for now)
    const botResponse = {
      id: messages.length + 2,
      type: "bot",
      content:
        "This is a placeholder response. The backend integration will be implemented later.",
      timestamp: new Date(),
    };

    setMessages([...messages, userMessage, botResponse]);
    setInputMessage("");
  };

  return (
    <div className="h-full flex flex-col bg-emerald-50">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto py-6 px-4 sm:px-6">
        <div className="space-y-6">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.type === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`inline-block px-4 py-2 rounded-xl shadow-sm max-w-[80%] sm:max-w-[70%] 
                  ${
                    message.type === "user"
                      ? "bg-emerald-700 text-white"
                      : "bg-white text-emerald-900"
                  }`}
              >
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                <p
                  className={`text-[10px] mt-1 ${
                    message.type === "user"
                      ? "text-emerald-200"
                      : "text-emerald-500"
                  }`}
                >
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Input area */}
      <div className="border-t border-emerald-900/10 bg-white px-4 py-4 sm:px-6">
        <form onSubmit={handleSubmit} className="flex space-x-4">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask me anything about taxes..."
            className="flex-1 min-w-0 rounded-xl border-0 bg-emerald-50 px-4 py-3 text-emerald-900 shadow-sm ring-1 ring-inset ring-emerald-300 placeholder:text-emerald-400 focus:ring-2 focus:ring-inset focus:ring-emerald-600 sm:text-sm"
          />
          <button
            type="submit"
            disabled={!inputMessage.trim()}
            className={`rounded-xl px-4 flex items-center justify-center transition-colors ${
              inputMessage.trim()
                ? "bg-emerald-700 text-white hover:bg-emerald-800 shadow-sm"
                : "bg-emerald-100 text-emerald-400 cursor-not-allowed"
            }`}
          >
            <PaperAirplaneIcon className="h-5 w-5" />
          </button>
        </form>
      </div>
    </div>
  );
}
