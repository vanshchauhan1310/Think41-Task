import React from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';
import { useChat } from '../context/ChatContext';

const ChatWindow = () => {
  const { messages, loading, input, setInput, sendMessage } = useChat();

  return (
    <div className="chat-window p-4 w-full max-w-md bg-white rounded shadow-md">
      <h3 className="font-semibold text-lg mb-2">Chat Support</h3>
      {loading && (
        <div className="text-center py-2 text-gray-600">
          <div className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
          <span className="ml-2">AI is thinking...</span>
        </div>
      )}
      <MessageList messages={messages} />
      <UserInput input={input} setInput={setInput} sendMessage={sendMessage} />
    </div>
  );
};

export default ChatWindow;
