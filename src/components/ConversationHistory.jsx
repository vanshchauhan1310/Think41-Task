import React from 'react';
import { useChat } from '../context/ChatContext';

const ConversationHistory = () => {
  const { 
    conversations, 
    currentConversationId, 
    loadConversation, 
    startNewConversation 
  } = useChat();

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = (now - date) / (1000 * 60 * 60);
    
    if (diffInHours < 24) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffInHours < 48) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString();
    }
  };

  const handleConversationClick = (conversation) => {
    loadConversation(conversation);
  };

  const handleNewConversation = () => {
    startNewConversation();
  };

  return (
    <div className="conversation-history bg-gray-50 border-r border-gray-200 w-64 p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-gray-800">Conversations</h3>
        <button
          onClick={handleNewConversation}
          className="text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          New Chat
        </button>
      </div>
      
      <div className="space-y-2">
        {conversations.map((conversation) => (
          <div
            key={conversation.id}
            onClick={() => handleConversationClick(conversation)}
            className={`p-3 rounded-lg cursor-pointer transition-colors ${
              currentConversationId === conversation.id
                ? 'bg-blue-100 border border-blue-300'
                : 'bg-white hover:bg-gray-100 border border-gray-200'
            }`}
          >
            <div className="font-medium text-sm text-gray-800 truncate">
              {conversation.title}
            </div>
            <div className="text-xs text-gray-500 mt-1">
              {formatDate(conversation.timestamp)}
            </div>
            <div className="text-xs text-gray-600 mt-1 truncate">
              {conversation.messages.length > 1 
                ? `${conversation.messages.length - 1} messages`
                : 'No messages yet'
              }
            </div>
          </div>
        ))}
        
        {conversations.length === 0 && (
          <div className="text-center text-gray-500 text-sm py-4">
            No conversations yet
          </div>
        )}
      </div>
    </div>
  );
};

export default ConversationHistory; 