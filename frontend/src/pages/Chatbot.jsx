import React, { useState } from 'react';
import { motion } from 'framer-motion';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [branch, setBranch] = useState('CSE');
  const [subject, setSubject] = useState('');
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages(prev => [...prev, { text: input, sender: 'user' }]);
    setLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/chat/chatbot?query=${encodeURIComponent(input)}&branch=${branch}&subject=${encodeURIComponent(subject)}`);
      const data = await response.json();
      const isAIGenerated = (!data.examples || data.examples.length === 0) && (!data.formulas || data.formulas.length === 0);

      const newMessages = [
        { text: data.answer || "No response from chatbot", sender: 'bot', aiGenerated: isAIGenerated },
        ...(data.examples || []).map(ex => ({ text: `📘 Example: ${ex}`, sender: 'bot' })),
        ...(data.formulas || []).map(fm => ({ text: `🧮 Formula: ${fm}`, sender: 'bot' }))
      ];

      setMessages(prev => [...prev, ...newMessages]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages(prev => [...prev, { text: "⚠️ Error fetching response from backend.", sender: 'bot' }]);
    }

    setInput('');
    setLoading(false);
  };

  const handleExport = () => {
    const content = messages.map(msg => `${msg.sender === 'user' ? 'You' : 'AcadeMate'}: ${msg.text}`).join('\n');
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'academate_chat_history.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  const toggleTheme = () => setDarkMode(!darkMode);
  const styles = darkMode ? darkStyles : lightStyles;

  return (
    <div className={`chat-container ${darkMode ? 'dark' : 'light'}`} style={styles.container}>
      <h2 style={styles.title}>AcadeMate</h2>

      <div style={styles.controlsWrapper}>
        <select value={branch} onChange={(e) => setBranch(e.target.value)} style={styles.select}>
          <option value="CSE">CSE</option>
          <option value="ECE">ECE</option>
          <option value="EEE">EEE</option>
          <option value="MCH">MCH</option>
          <option value="CE">CE</option>
          <option value="CHE">CHE</option>
        </select>

        <input
          type="text"
          placeholder="Optional: Enter Subject Name"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          style={styles.input}
        />

        <button onClick={toggleTheme} style={styles.button}>
          {darkMode ? '☀️ Light Mode' : '🌙 Dark Mode'}
        </button>

        <button onClick={handleExport} style={styles.button}>
          📁 Export Chat
        </button>
      </div>

      <div style={styles.chatBox}>
        {messages.map((msg, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            style={msg.sender === 'user' ? styles.userMsg : styles.botMsg}
          >
            {msg.text}
            {msg.aiGenerated && <span style={styles.tag}> 🤖 AI-generated</span>}
          </motion.div>
        ))}
        {loading && <div style={styles.botMsg}>Typing...</div>}
      </div>

      <div style={styles.controls}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask your KTU doubt..."
          style={styles.input}
        />
        <button onClick={handleSend} style={styles.button} disabled={loading}>Send</button>
      </div>
    </div>
  );
};

const baseStyles = {
  container: {
    padding: '20px',
    maxWidth: '900px',
    margin: 'auto',
    fontFamily: 'sans-serif',
    borderRadius: '12px',
  },
  title: {
    textAlign: 'center',
    marginBottom: '15px',
    fontSize: '2rem',
    fontWeight: 'bold',
  },
  chatBox: {
    border: '1px solid #ccc',
    borderRadius: '10px',
    padding: '15px',
    height: '500px',
    overflowY: 'auto',
    marginBottom: '12px',
  },
  userMsg: {
    textAlign: 'right',
    padding: '10px',
    margin: '6px 0',
    borderRadius: '10px',
  },
  botMsg: {
    textAlign: 'left',
    padding: '10px',
    margin: '6px 0',
    borderRadius: '10px',
  },
  controls: {
    display: 'flex',
    gap: '10px',
    marginBottom: '10px',
  },
  input: {
    flexGrow: 1,
    padding: '10px',
    borderRadius: '8px',
    border: '1px solid #ccc',
  },
  button: {
    padding: '10px 14px',
    borderRadius: '8px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    cursor: 'pointer',
  },
  select: {
    padding: '10px',
    borderRadius: '8px',
    border: '1px solid #ccc',
  },
  tag: {
    fontSize: '0.75rem',
    color: '#666',
    marginLeft: '6px',
  },
  controlsWrapper: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '10px',
    justifyContent: 'center',
    marginBottom: '12px',
  },
};

const lightStyles = {
  ...baseStyles,
  container: { ...baseStyles.container, backgroundColor: '#fefefe', color: '#000' },
  userMsg: { ...baseStyles.userMsg, backgroundColor: '#d1e7dd' },
  botMsg: { ...baseStyles.botMsg, backgroundColor: '#e2e3e5' },
};

const darkStyles = {
  ...baseStyles,
  container: { ...baseStyles.container, backgroundColor: '#1e1e1e', color: '#f1f1f1' },
  userMsg: { ...baseStyles.userMsg, backgroundColor: '#2c3e50' },
  botMsg: { ...baseStyles.botMsg, backgroundColor: '#34495e' },
  input: { ...baseStyles.input, backgroundColor: '#2d2d2d', color: '#f1f1f1', border: '1px solid #555' },
  button: { ...baseStyles.button, backgroundColor: '#2980b9' },
  select: { ...baseStyles.select, backgroundColor: '#2d2d2d', color: '#f1f1f1', border: '1px solid #555' },
};

export default Chatbot;
