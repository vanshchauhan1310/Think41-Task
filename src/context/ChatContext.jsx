import React, { createContext, useContext, useReducer } from 'react';

// Initial state
const initialState = {
  messages: [
    { from: 'bot', text: 'Hi! How can I help you today?' }
  ],
  loading: false,
  input: ''
};

// Action types
const ACTIONS = {
  SET_MESSAGES: 'SET_MESSAGES',
  ADD_MESSAGE: 'ADD_MESSAGE',
  SET_LOADING: 'SET_LOADING',
  SET_INPUT: 'SET_INPUT',
  CLEAR_INPUT: 'CLEAR_INPUT'
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
    sendMessage
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