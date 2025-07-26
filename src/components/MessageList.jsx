import React from 'react';
import Message from './Message';

const MessageList = ({ messages }) => (
  <div className="h-64 overflow-y-auto border rounded p-2 mb-2 bg-gray-50">
    {messages.map((msg, i) => (
      <Message key={i} from={msg.from} text={msg.text} />
    ))}
  </div>
);

export default MessageList; 