import React, { useRef, useEffect, useState } from 'react';
import './App.css';


const App = () => {
  const videoRef = useRef(null);
  const chatRef = useRef(null);
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');
  const [chatInput, setChatInput] = useState('');
  const [chatMessages, setChatMessages] = useState([]);
  const ws = useRef(null);

  useEffect(() => {
    // Webcam setup
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => videoRef.current.srcObject = stream)
      .catch(err => console.error('Webcam error:', err));

    // WebSocket setup
    ws.current = new WebSocket('ws://localhost:5000');
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setChatMessages(prev => [...prev, { type: 'bot', text: data.reply }]);
    };

    return () => ws.current?.close();
  }, []);

  useEffect(() => {
    // Scroll chat to bottom on new message
    chatRef.current?.scrollTo({ top: chatRef.current.scrollHeight, behavior: 'smooth' });
  }, [chatMessages]);

  const captureImage = () => {
    const canvas = document.createElement('canvas');
    canvas.width = 640;
    canvas.height = 480;
    canvas.getContext('2d').drawImage(videoRef.current, 0, 0);
    return canvas.toDataURL('image/jpeg');
  };

  const handleRegister = async () => {
    const image = captureImage();
    const res = await fetch('http://localhost:5000/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, image }),
    });
    const data = await res.json();
    setMessage(data.message);
  };

  const handleRecognize = async () => {
    const image = captureImage();
    const res = await fetch('http://localhost:5000/api/recognize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image }),
    });
    const data = await res.json();
    setMessage(data.message || `Welcome __ ${data.name} `);
  };

  const handleChatSend = () => {
    if (!chatInput.trim()) return;
    ws.current.send(JSON.stringify({ query: chatInput }));
    setChatMessages(prev => [...prev, { type: 'user', text: chatInput }]);
    setChatInput('');
  };

  const handleSuggestion = (text) => {
    setChatInput(text);
    handleChatSend();
  };

  const suggestions = [
    "hello",
    "Who was the last person registered?",
    "How many users are registered?",
    "Who registered more than once?",
    "Who registered first?",
    "hi"
  ];

  return (
    <div className="app-container">
      <h1 className="app-title">FaceIQ</h1>

      <div className="video-box">
        <video ref={videoRef} autoPlay width="640" height="480" />
        <div className="video-controls">
          <input
            placeholder="Enter name"
            value={name}
            onChange={e => setName(e.target.value)}
          />
          <button onClick={handleRegister} className="register">Register</button>
          <button onClick={handleRecognize} className="recognize">Recognize</button>
        </div>
        <p className="message">{message}</p>
      </div>

      <div className="chat-section">
        <h2 className="chat-title">Ask Anything</h2>
        <div ref={chatRef} className="chat-history">
          {chatMessages.map((msg, idx) => (
            <div key={idx} className={`chat-message ${msg.type}`}>
              <span className={`chat-bubble ${msg.type}`}>
                <strong>{msg.type === 'user' ? 'You' : 'Bot'}:</strong> {msg.text}
              </span>
            </div>
          ))}
        </div>

        <div className="chat-input-area">
          <input
            type="text"
            value={chatInput}
            onChange={e => setChatInput(e.target.value)}
            placeholder="Type your question..."
            onKeyDown={(e) => e.key === 'Enter' && handleChatSend()}
          />
          <button onClick={handleChatSend}>Send</button>
        </div>

        <div className="suggestions">
          {suggestions.map((s, idx) => (
            <button key={idx} onClick={() => handleSuggestion(s)}>
              {s}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default App;
