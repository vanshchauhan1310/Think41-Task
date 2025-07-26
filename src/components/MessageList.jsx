import React from 'react';
import Message from './Message';

const MessageList = ({ messages }) => (
  <div className="h-full overflow-y-auto p-4 bg-gray-50">
    {messages.map((msg, i) => (
      <Message key={i} from={msg.from} text={msg.text} />
    ))}
  </div>
);

export default MessageList; 