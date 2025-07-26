import React, { useState } from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';

const ChatWindow = () => {
  const [messages, setMessages] = useState([
    { from: 'bot', text: 'Hi! How can I help you today?' }
  ]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { from: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    try {
      const res = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { from: 'bot', text: data.reply }]);
    } catch (err) {
      setMessages(prev => [...prev, { from: 'bot', text: 'Error contacting server.' }]);
    }
  };

  return (
    <div className="chat-window p-4 w-full max-w-md bg-white rounded shadow-md">
      <h3 className="font-semibold text-lg mb-2">Chat Support</h3>
      <MessageList messages={messages} />
      <UserInput input={input} setInput={setInput} sendMessage={sendMessage} />
    </div>
  );
};

export default ChatWindow;
