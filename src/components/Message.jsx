import React from 'react';

const Message = ({ from, text }) => (
  <div
    className={`p-2 rounded my-1 max-w-xs text-sm ${
      from === 'user' ? 'bg-blue-200 ml-auto text-right' : 'bg-gray-200 mr-auto text-left'
    }`}
  >
    {text}
  </div>
);

export default Message; 