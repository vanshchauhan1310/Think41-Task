import React from 'react';

const UserInput = ({ input, setInput, sendMessage }) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage(input);
    }
  };

  const handleSendClick = () => {
    sendMessage(input);
  };

  return (
    <div className="flex gap-2">
      <input
        type="text"
        placeholder="Ask something..."
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={handleKeyPress}
        className="flex-1 px-3 py-2 border rounded focus:outline-none"
      />
      <button
        onClick={handleSendClick}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Send
      </button>
    </div>
  );
};

export default UserInput; 