import React, { createContext, useContext, useReducer, useEffect } from 'react';

// Placeholder user ID (replace with real auth/user logic as needed)
const USER_ID = 'demo-user-123';

// Initial state
const initialState = {
  messages: [
    { from: 'bot', text: 'Hi! How can I help you today?' }
  ],
  loading: false,
  input: '',
  conversations: [],
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
  START_NEW_CONVERSATION: 'START_NEW_CONVERSATION',
  SET_CURRENT_CONVERSATION_ID: 'SET_CURRENT_CONVERSATION_ID'
};

// Reducer function
const chatReducer = (state, action) => {
  switch (action.type) {
    case ACTIONS.SET_MESSAGES:
      return { ...state, messages: action.payload };
    case ACTIONS.ADD_MESSAGE:
      return { ...state, messages: [...state.messages, action.payload] };
    case ACTIONS.SET_LOADING:
      return { ...state, loading: action.payload };
    case ACTIONS.SET_INPUT:
      return { ...state, input: action.payload };
    case ACTIONS.CLEAR_INPUT:
      return { ...state, input: '' };
    case ACTIONS.SET_CONVERSATIONS:
      return { ...state, conversations: action.payload };
    case ACTIONS.ADD_CONVERSATION:
      return { ...state, conversations: [action.payload, ...state.conversations] };
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
    case ACTIONS.SET_CURRENT_CONVERSATION_ID:
      return { ...state, currentConversationId: action.payload };
    default:
      return state;
  }
};

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  // Fetch all conversations for the user on mount
  useEffect(() => {
    fetchConversations();
  }, []);

  // Fetch conversations from backend
  const fetchConversations = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/conversations/user/${USER_ID}`);
      const data = await res.json();
      dispatch({ type: ACTIONS.SET_CONVERSATIONS, payload: data });
    } catch (err) {
      // Optionally handle error
      dispatch({ type: ACTIONS.SET_CONVERSATIONS, payload: [] });
    }
  };

  // Load a specific conversation from backend
  const loadConversation = async (conversation) => {
    try {
      const res = await fetch(`http://localhost:8000/api/conversations/${conversation.id}`);
      const data = await res.json();
      dispatch({ type: ACTIONS.LOAD_CONVERSATION, payload: data });
    } catch (err) {
      // Optionally handle error
    }
  };

  // Start a new conversation
  const startNewConversation = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/conversations/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: USER_ID })
      });
      const data = await res.json();
      dispatch({ type: ACTIONS.START_NEW_CONVERSATION });
      dispatch({ type: ACTIONS.SET_CURRENT_CONVERSATION_ID, payload: data.id });
      fetchConversations();
    } catch (err) {
      dispatch({ type: ACTIONS.START_NEW_CONVERSATION });
    }
  };

  // Send a message to the backend chat API
  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return;
    dispatch({ type: ACTIONS.SET_LOADING, payload: true });
    const userMessage = { from: 'user', text: messageText };
    dispatch({ type: ACTIONS.ADD_MESSAGE, payload: userMessage });
    dispatch({ type: ACTIONS.CLEAR_INPUT });
    try {
      const res = await fetch(`http://localhost:8000/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_message: messageText,
          user_id: USER_ID,
          conversation_id: state.currentConversationId
        })
      });
      const data = await res.json();
      // The backend returns the updated conversation, so update messages and conversation id
      dispatch({ type: ACTIONS.SET_MESSAGES, payload: data.messages });
      dispatch({ type: ACTIONS.SET_CURRENT_CONVERSATION_ID, payload: data.id });
      fetchConversations();
    } catch (err) {
      dispatch({ type: ACTIONS.ADD_MESSAGE, payload: { from: 'bot', text: 'Error contacting server.' } });
    } finally {
      dispatch({ type: ACTIONS.SET_LOADING, payload: false });
    }
  };

  const setInput = (input) => {
    dispatch({ type: ACTIONS.SET_INPUT, payload: input });
  };

  const clearInput = () => {
    dispatch({ type: ACTIONS.CLEAR_INPUT });
  };

  const value = {
    ...state,
    setInput,
    clearInput,
    sendMessage,
    loadConversation,
    startNewConversation,
    fetchConversations,
    USER_ID
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};
