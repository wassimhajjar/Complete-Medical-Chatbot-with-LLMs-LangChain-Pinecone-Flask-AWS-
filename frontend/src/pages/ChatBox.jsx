import React, { useState, useEffect, useRef } from "react";
import { useAppContext } from "../context/AppContext";
import toast from "react-hot-toast";
import "../assets/App.css";

function ChatBox() {
  const { messages, setMessages, user, axios, token } = useAppContext();
  const containerRef = useRef(null);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTo({
        top: containerRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages]);

  const onSubmit = async (e) => {
    try {
      e.preventDefault();
      if (!user) {
        return toast("Login to send message");
      }
      setLoading(true);
      const promptCopy = prompt;
      setPrompt("");
      setMessages((prev) => [
        ...prev,
        {
          role: "human",
          content: promptCopy,
          timestamps: Date.now(),
        },
      ]);
      const { data } = await axios.post(
        "/messages",
        { role: "human", content: promptCopy },
        { headers: { Authorization: token } },
      );
      if (data) {
        console.log("data", data.id);
        setMessages((prev) => [...prev, data]);
      } else {
        toast.error(data);
        setPrompt(promptCopy);
      }
    } catch (error) {
      toast.error(error);
    } finally {
      setPrompt("");
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Medical ChatBot</h1>
      <div ref={containerRef} className="chat-window">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            {message.content}
          </div>
        ))}
        {loading && <div className="message ai">Loading...</div>}
      </div>
      <form onSubmit={onSubmit} className="chat-form">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatBox;
