import React, { useState } from "react";
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProductList from './components/ProductList';
import ChatWindow from './components/ChatWindow';
import './App.css';

export default function App() {
  const [chatOpen, setChatOpen] = useState(false);

  const toggleChat = () => {
    setChatOpen(!chatOpen);
  };

  return (
    <div className="app">
      <Navbar toggleChat={toggleChat} />

      <main className="content">
        <Routes>
          <Route path="/" element={<ProductList />} />
          <Route path="/products" element={<ProductList />} />
          <Route path="/products/:category" element={<ProductList />} />
        </Routes>
      </main>

      <div className={`chatbot-container ${chatOpen ? 'open' : ''}`}>
        {chatOpen && <ChatWindow />}
        <button
          className="chatbot-toggle"
          onClick={toggleChat}
          aria-label={chatOpen ? 'Close chat' : 'Open chat'}
        >
          {chatOpen ? '✕' : '💬'}
        </button>
      </div>
    </div>
  );
}
