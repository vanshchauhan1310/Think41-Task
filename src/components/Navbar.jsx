import React from 'react';
import { Link } from 'react-router-dom';

export default function Navbar({ toggleChat }) {
  return (
    <nav className="navbar">
      <div className="navbar-logo">EcoRmarce</div>
      <ul className="navbar-links">
        <li><Link to="/">Home</Link></li>
        <li><Link to="/products">Products</Link></li>
      </ul>
      <button className="chat-toggle" onClick={toggleChat}>💬 Chat</button>
    </nav>
  );
}
