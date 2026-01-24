import React, { useState, useEffect, useRef } from "react";
import { useAppContext } from "../context/AppContext";
import toast from "react-hot-toast";
import "../assets/App.css";

function ChatBox() {
  const { messages, setMessages, user, axios, token } = useAppContext();
  const containerRef = useRef(null);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  // Effect to load chat history from local storage when the app starts
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
  // const handleSubmit = async (event) => {
  //   event.preventDefault();
  //   if (!userInput.trim()) return; // Don't send empty messages

  //   const userMessage = { type: "user", text: userInput };
  //   const newChatLog = [...chatLog, userMessage];
  //   setChatLog(newChatLog);
  //   setUserInput("");
  //   setLoading(true);

  //   try {
  //     // The API call to our FastAPI backend
  //     const response = await fetch("http://localhost:8000/chat", {
  //       method: "POST",
  //       headers: { "Content-Type": "application/json" },
  //       body: JSON.stringify({ user_message: userInput }),
  //     });

  //     if (!response.ok) {
  //       throw new Error(`HTTP error! status: ${response.status}`);
  //     }

  //     const data = await response.json();
  //     const botMessage = { type: "bot", text: data.bot_response };

  //     // Update the chat log with the bot's response
  //     const finalChatLog = [...newChatLog, botMessage];
  //     setChatLog(finalChatLog);

  //     // Save the updated chat log to local storage for persistence
  //     localStorage.setItem("chatLog", JSON.stringify(finalChatLog));
  //   } catch (error) {
  //     console.error("Error fetching chat response:", error);
  //     const errorMessage = {
  //       type: "error",
  //       text: "Sorry, something went wrong. Please try again.",
  //     };
  //     setChatLog((prev) => [...prev, errorMessage]);
  //   } finally {
  //     setLoading(false);
  //   }
  // };

  return (
    console.log("messages final", messages),
    (
      <div className="App">
        <h1>Medical Chatbot</h1>
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
    )
  );
}

export default ChatBox;
