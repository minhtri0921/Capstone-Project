import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles/Chatbox.css";

const Chatbox = () => {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState(() => {
    // Load chat history from localStorage on component mount
    const savedMessages = localStorage.getItem("chatHistory");
    return savedMessages ? JSON.parse(savedMessages) : [];
  });

  useEffect(() => {
    // Save chat history to localStorage whenever it changes
    localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
  }, [chatHistory]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const newMessage = { content: message, type: "human" };

    // Update chat history with the new human message
    setChatHistory((prev) => [...prev, newMessage]);

    try {
      const response = await axios.post("http://127.0.0.1:8000/chat", {
        language: "vi",
        messages: chatHistory.concat(newMessage).map(({ content, type }) => ({
          content,
          type,
        })),
      });
      setMessage("");
      const botMessage = {
        content: response.data || "Xin lỗi, tôi không thể trả lời câu hỏi này.",
        type: "ai",
      };

      // Update chat history with the bot's response
      setChatHistory((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error sending message: ", error);

      const botMessage = {
        content: "Có lỗi xảy ra khi gửi tin nhắn. Vui lòng thử lại.",
        type: "ai",
      };

      // Update chat history with the error message
      setChatHistory((prev) => [...prev, botMessage]);
    }

    // Clear the input field
    setMessage("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="chatbox">
      <div className="chatbox-header">Chat with Us</div>
      <div className="chatbox-body">
        {chatHistory.map((msg, index) => (
          <div
            key={index}
            className={`chatbox-message ${
              msg.type === "human" ? "human" : "bot"
            }`}
          >
            {msg.type === "ai" && (
              <>
                <img
                  src="/13330989.png"
                  alt="Bot Avatar"
                  className="chatbox-avatar"
                />
                <span className="chatbox-content">{msg.content}</span>
              </>
            )}
            {msg.type === "human" && (
              <>
                <span className="chatbox-content">{msg.content}</span>
                <img
                  src="/210901.jpg"
                  alt="User Avatar"
                  className="chatbox-avatar"
                />
              </>
            )}
          </div>
        ))}
      </div>

      <div className="chatbox-footer">
        <input
          type="text"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chatbox;
