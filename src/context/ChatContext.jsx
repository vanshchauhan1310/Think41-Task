import React, { createContext, useContext, useReducer } from 'react';

// Initial state
const initialState = {
  messages: [
    { from: 'bot', text: 'Hi! How can I help you today?' }
  ],
  loading: false,
  input: '',
  conversations: [
    {
      id: '1',
      title: 'Product Inquiry',
      timestamp: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
      messages: [
        { from: 'bot', text: 'Hi! How can I help you today?' },
        { from: 'user', text: 'I need help finding a t-shirt' },
        { from: 'bot', text: 'I can help you find the perfect t-shirt! What size and color are you looking for?' },
        { from: 'user', text: 'Large, blue' },
        { from: 'bot', text: 'Great! I found several blue t-shirts in large size. Would you like me to show you the options?' }
      ]
    },
    {
      id: '2',
      title: 'Order Status',
      timestamp: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
      messages: [
        { from: 'bot', text: 'Hi! How can I help you today?' },
        { from: 'user', text: 'I want to check my order status' },
        { from: 'bot', text: 'I can help you check your order status. Please provide your order number.' },
        { from: 'user', text: 'ORD-12345' },
        { from: 'bot', text: 'Your order ORD-12345 is currently being processed and will be shipped within 2-3 business days.' }
      ]
    }
  ],
  currentConversationId: null
};

// Action types
const ACTIONS = {
  SET_MESSAGES: 'SET_MESSAGES',
  ADD_MESSAGE: 'ADD_MESSAGE',
  SET_LOADING: 'SET_LOADING',
  SET_INPUT: 'SET_INPUT',
  CLEAR_INPUT: 'CLEAR_INPUT',
  SET_CONVERSATIONS: 'SET_CONVERSATIONS',
  ADD_CONVERSATION: 'ADD_CONVERSATION',
  LOAD_CONVERSATION: 'LOAD_CONVERSATION',
  START_NEW_CONVERSATION: 'START_NEW_CONVERSATION'
};

// Reducer function
const chatReducer = (state, action) => {
  switch (action.type) {
    case ACTIONS.SET_MESSAGES:
      return { ...state, messages: action.payload };
    
    case ACTIONS.ADD_MESSAGE:
      return { 
        ...state, 
        messages: [...state.messages, action.payload] 
      };
    
    case ACTIONS.SET_LOADING:
      return { ...state, loading: action.payload };
    
    case ACTIONS.SET_INPUT:
      return { ...state, input: action.payload };
    
    case ACTIONS.CLEAR_INPUT:
      return { ...state, input: '' };
    
    case ACTIONS.SET_CONVERSATIONS:
      return { ...state, conversations: action.payload };
    
    case ACTIONS.ADD_CONVERSATION:
      return { 
        ...state, 
        conversations: [action.payload, ...state.conversations] 
      };
    
    case ACTIONS.LOAD_CONVERSATION:
      return { 
        ...state, 
        messages: action.payload.messages,
        currentConversationId: action.payload.id
      };
    
    case ACTIONS.START_NEW_CONVERSATION:
      return { 
        ...state, 
        messages: [{ from: 'bot', text: 'Hi! How can I help you today?' }],
        currentConversationId: null
      };
    
    default:
      return state;
  }
};

// Create context
const ChatContext = createContext();

// Provider component
export const ChatProvider = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  // Actions
  const addMessage = (message) => {
    dispatch({ type: ACTIONS.ADD_MESSAGE, payload: message });
  };

  const setLoading = (loading) => {
    dispatch({ type: ACTIONS.SET_LOADING, payload: loading });
  };

  const setInput = (input) => {
    dispatch({ type: ACTIONS.SET_INPUT, payload: input });
  };

  const clearInput = () => {
    dispatch({ type: ACTIONS.CLEAR_INPUT });
  };

  const loadConversation = (conversation) => {
    dispatch({ type: ACTIONS.LOAD_CONVERSATION, payload: conversation });
  };

  const startNewConversation = () => {
    dispatch({ type: ACTIONS.START_NEW_CONVERSATION });
  };

  const saveCurrentConversation = (title) => {
    if (state.messages.length <= 1) return; // Don't save if only welcome message
    
    const newConversation = {
      id: Date.now().toString(),
      title: title || `Conversation ${state.conversations.length + 1}`,
      timestamp: new Date().toISOString(),
      messages: state.messages
    };
    
    dispatch({ type: ACTIONS.ADD_CONVERSATION, payload: newConversation });
  };

  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return;

    // Add user message
    const userMessage = { from: 'user', text: messageText };
    addMessage(userMessage);
    clearInput();
    setLoading(true);

    try {
      const res = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: messageText }),
      });
      const data = await res.json();
      addMessage({ from: 'bot', text: data.reply });
    } catch (err) {
      addMessage({ from: 'bot', text: 'Error contacting server.' });
    } finally {
      setLoading(false);
    }
  };

  const value = {
    ...state,
    addMessage,
    setLoading,
    setInput,
    clearInput,
    sendMessage,
    loadConversation,
    startNewConversation,
    saveCurrentConversation
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

// Custom hook to use the chat context
export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}; 