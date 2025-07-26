import React, { useState } from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';
import ConversationHistory from './ConversationHistory';
import { useChat } from '../context/ChatContext';

const ChatWindow = () => {
  const { messages, loading, input, setInput, sendMessage } = useChat();
  const [showHistory, setShowHistory] = useState(true);

  return (
    <div className="chat-window bg-white rounded shadow-md flex h-96 max-w-4xl">
      {/* Conversation History Side Panel */}
      {showHistory && <ConversationHistory />}
      
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header with toggle button */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h3 className="font-semibold text-lg">Chat Support</h3>
          <button
            onClick={() => setShowHistory(!showHistory)}
            className="text-gray-600 hover:text-gray-800 p-2 rounded"
          >
            {showHistory ? '←' : '→'}
          </button>
        </div>
        
        {/* Loading indicator */}
        {loading && (
          <div className="text-center py-2 text-gray-600 border-b border-gray-200">
            <div className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            <span className="ml-2">AI is thinking...</span>
          </div>
        )}
        
        {/* Messages */}
        <div className="flex-1 overflow-hidden">
          <MessageList messages={messages} />
        </div>
        
        {/* Input */}
        <div className="p-4 border-t border-gray-200">
          <UserInput input={input} setInput={setInput} sendMessage={sendMessage} />
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
