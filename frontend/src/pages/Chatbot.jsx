import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';

const Chatbot = () => {
  const navigate = useNavigate();
  
  // Chat States
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  
  // Customization & Auth States
  const [branch, setBranch] = useState('CSE');
  const [semester, setSemester] = useState(3);
  const [scheme, setScheme] = useState('2019');
  const [subject, setSubject] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const [userName, setUserName] = useState('Student');

  // Academic Dashboard States
  const [syllabusSubjects, setSyllabusSubjects] = useState([]);
  const [syllabusLoading, setSyllabusLoading] = useState(false);
  const [qps, setQps] = useState([]);
  const [qpLoading, setQpLoading] = useState(false);
  
  // Curriculum Search States
  const [curriculumQuery, setCurriculumQuery] = useState('');
  const [curriculumResults, setCurriculumResults] = useState([]);
  const [curriculumLoading, setCurriculumLoading] = useState(false);
  const [subjectSearch, setSubjectSearch] = useState('');

  // Tab State for Mobile Responsiveness (Left Panel vs Right Panel)
  const [activeTab, setActiveTab] = useState('chat'); // 'chat' or 'academics'

  // Authentication Guard
  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    if (!token) {
      navigate('/');
    } else if (user) {
      try {
        const parsed = JSON.parse(user);
        if (parsed.name) setUserName(parsed.name);
      } catch (e) {
        console.error("Failed to parse user session info");
      }
    }
  }, [navigate]);

  // Fetch Syllabus and Question Papers on Branch/Semester/Scheme Change
  useEffect(() => {
    const fetchAcademicData = async () => {
      setSyllabusLoading(true);
      setQpLoading(true);
      try {
        // 1. Fetch Syllabus subjects
        const sylRes = await fetch(`http://localhost:8000/chat/syllabus?branch=${branch}&semester=${semester}&scheme=${scheme}`);
        const sylData = await sylRes.json();
        setSyllabusSubjects(sylData.subjects || []);

        // 2. Fetch Question Papers
        const qpRes = await fetch(`http://localhost:8000/chat/question-papers?branch=${branch}&semester=${semester}&scheme=${scheme}`);
        const qpData = await qpRes.json();
        setQps(qpData.question_papers || []);
      } catch (error) {
        console.error("Error fetching syllabus/QPs:", error);
      } finally {
        setSyllabusLoading(false);
        setQpLoading(false);
      }
    };

    if (localStorage.getItem('token')) {
      fetchAcademicData();
    }
  }, [branch, semester, scheme]);

  // Handle Sending Message to Chatbot
  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages(prev => [...prev, { text: input, sender: 'user' }]);
    setLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/chat/chatbot?query=${encodeURIComponent(input)}&branch=${branch}&subject=${encodeURIComponent(subject)}&scheme=${scheme}`);
      const data = await response.json();
      
      const isAIGenerated = data.source === 'AI';

      const newMessages = [
        { text: data.answer || "No response from chatbot", sender: 'bot', aiGenerated: isAIGenerated },
        ...(data.examples || []).map(ex => ({ text: `📘 Example: ${ex}`, sender: 'bot' })),
        ...(data.formulas || []).map(fm => ({ text: `🧮 Formula: ${fm}`, sender: 'bot' }))
      ];

      setMessages(prev => [...prev, ...newMessages]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages(prev => [...prev, { text: "⚠️ Error fetching response from backend. Check connection.", sender: 'bot' }]);
    }

    setInput('');
    setLoading(false);
  };

  // Search through parsed PDF Curriculum texts
  const handleCurriculumSearch = async (e) => {
    e.preventDefault();
    if (!curriculumQuery.trim()) return;
    setCurriculumLoading(true);
    setCurriculumResults([]);

    try {
      const res = await fetch(`http://localhost:8000/chat/curriculum-search?query=${encodeURIComponent(curriculumQuery)}&scheme=${scheme}&branch=${branch}&subject=${encodeURIComponent(subject)}`);
      const data = await res.json();
      setCurriculumResults(data.results || ["No matches found in the curriculum PDF."]);
    } catch (error) {
      console.error("Curriculum search error:", error);
      setCurriculumResults(["⚠️ Failed to query curriculum search API."]);
    } finally {
      setCurriculumLoading(false);
    }
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

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/');
  };

  const toggleTheme = () => setDarkMode(!darkMode);
  const styles = darkMode ? darkStyles : lightStyles;

  const filteredSubjects = syllabusSubjects.filter(sub =>
    sub.name.toLowerCase().includes(subjectSearch.toLowerCase()) ||
    sub.code.toLowerCase().includes(subjectSearch.toLowerCase())
  );

  return (
    <div className={`app-wrapper ${darkMode ? 'dark-theme' : 'light-theme'}`} style={styles.appWrapper}>
      {/* HEADER SECTION */}
      <header style={styles.header}>
        <div style={styles.logoGroup}>
          <span style={styles.logoIcon}>🎓</span>
          <div>
            <h1 style={styles.headerTitle}>AcadeMate</h1>
            <p style={styles.headerSubtitle}>KTU AI-Tutor & Academic Portal</p>
          </div>
        </div>

        <div style={styles.userStatus}>
          <span>Welcome, <strong>{userName}</strong></span>
          <button onClick={toggleTheme} style={styles.iconBtn}>
            {darkMode ? '☀️ Light' : '🌙 Dark'}
          </button>
          <button onClick={handleExport} style={styles.actionBtn}>
            📁 Export
          </button>
          <button onClick={handleLogout} style={styles.logoutBtn}>
            🚪 Logout
          </button>
        </div>
      </header>

      {/* MOBILE TABS */}
      <div style={styles.mobileTabs}>
        <button 
          onClick={() => setActiveTab('chat')} 
          style={activeTab === 'chat' ? styles.activeMobileTab : styles.mobileTab}
        >
          💬 AI Chat Tutor
        </button>
        <button 
          onClick={() => setActiveTab('academics')} 
          style={activeTab === 'academics' ? styles.activeMobileTab : styles.mobileTab}
        >
          📚 Syllabus & Papers
        </button>
      </div>

      <div style={styles.mainContainer}>
        {/* LEFT COLUMN: ACADEMICS PORTAL (Syllabus, QPs, Search) */}
        <aside style={{
          ...styles.sidebar,
          display: activeTab === 'academics' ? 'flex' : (window.innerWidth <= 768 ? 'none' : 'flex')
        }}>
          {/* selectors */}
          <div style={styles.selectionCard}>
            <h3 style={styles.sectionHeading}>Academic Filters</h3>
            <div style={styles.selectorGroup}>
              <div style={styles.selectorField}>
                <label style={styles.label}>Branch</label>
                <select value={branch} onChange={(e) => setBranch(e.target.value)} style={styles.select}>
                  <option value="CSE">CSE</option>
                  <option value="ECE">ECE</option>
                  <option value="EEE">EEE</option>
                  <option value="ME">ME</option>
                  <option value="CE">CE</option>
                </select>
              </div>

              <div style={styles.selectorField}>
                <label style={styles.label}>Semester</label>
                <select value={semester} onChange={(e) => setSemester(Number(e.target.value))} style={styles.select}>
                  <option value="1">S1</option>
                  <option value="2">S2</option>
                  <option value="3">S3</option>
                  <option value="4">S4</option>
                  <option value="5">S5</option>
                  <option value="6">S6</option>
                  <option value="7">S7</option>
                  <option value="8">S8</option>
                </select>
              </div>

              <div style={styles.selectorField}>
                <label style={styles.label}>Scheme</label>
                <select value={scheme} onChange={(e) => setScheme(e.target.value)} style={styles.select}>
                  <option value="2019">2019</option>
                  <option value="2024">2024</option>
                </select>
              </div>
            </div>
          </div>

          {/* Syllabus Section */}
          <div style={styles.academicCard}>
            <h3 style={styles.sectionHeading}>📚 Syllabus Subjects</h3>
            <input 
              type="text" 
              placeholder="Search specific syllabus / subjects..." 
              value={subjectSearch} 
              onChange={(e) => setSubjectSearch(e.target.value)}
              style={{
                padding: '8px 12px',
                borderRadius: '6px',
                border: '1px solid #ccc',
                marginBottom: '8px',
                fontSize: '0.8rem',
                width: '100%',
                boxSizing: 'border-box',
                background: darkMode ? '#2d2d2d' : '#ffffff',
                color: darkMode ? '#ffffff' : '#000000'
              }}
            />
            {syllabusLoading ? (
              <p style={styles.infoText}>Loading subjects...</p>
            ) : filteredSubjects.length > 0 ? (
              <div style={styles.subjectList}>
                {filteredSubjects.map((sub, i) => (
                  <div 
                    key={i} 
                    onClick={() => {
                      setSubject(sub.name);
                      setInput(`Explain core topics in ${sub.name} (${sub.code})`);
                    }} 
                    style={{
                      ...styles.subjectItem,
                      borderLeft: subject === sub.name ? '4px solid #0078ff' : '4px solid transparent',
                      background: subject === sub.name ? 'rgba(0, 120, 255, 0.1)' : 'transparent'
                    }}
                  >
                    <div style={styles.subjectName}>{sub.name}</div>
                    <div style={styles.subjectCode}>{sub.code}</div>
                  </div>
                ))}
              </div>
            ) : (
              <p style={styles.infoText}>
                {syllabusSubjects.length > 0 ? "No subjects match your search." : `No subjects stored for ${branch} Semester ${semester}.`}
              </p>
            )}
          </div>


          {/* Question Papers Section */}
          <div style={styles.academicCard}>
            <h3 style={styles.sectionHeading}>🗂️ Sample Question Papers</h3>
            {qpLoading ? (
              <p style={styles.infoText}>Loading question papers...</p>
            ) : qps.length > 0 ? (
              <div style={styles.qpList}>
                {qps.map((qp, i) => (
                  <div key={i} style={styles.qpItem}>
                    <div style={styles.qpHeader}>
                      <span style={styles.qpSubject}>{qp.subject}</span>
                      <span style={styles.qpYear}>{qp.year} ({qp.exam_type})</span>
                    </div>
                    <ul style={styles.qpQuestions}>
                      {qp.questions.map((q, idx) => (
                        <li key={idx} style={styles.qpQuestionText} onClick={() => setInput(q)}>
                          "{q}"
                        </li>
                      ))}
                    </ul>
                    <a href={qp.pdf_url} target="_blank" rel="noreferrer" style={styles.downloadLink}>
                      📥 Download Full PDF
                    </a>
                  </div>
                ))}
              </div>
            ) : (
              <p style={styles.infoText}>No question papers found for {branch} Semester {semester}.</p>
            )}
          </div>

          {/* PDF Curriculum Search Section */}
          <div style={styles.academicCard}>
            <h3 style={styles.sectionHeading}>🔍 Search Curriculum PDFs</h3>
            <form onSubmit={handleCurriculumSearch} style={styles.searchForm}>
              <input
                type="text"
                placeholder="Search PDF topics (e.g. Trees, AVL...)"
                value={curriculumQuery}
                onChange={(e) => setCurriculumQuery(e.target.value)}
                style={styles.searchBar}
              />
              <button type="submit" style={styles.searchSubmit} disabled={curriculumLoading}>
                Search
              </button>
            </form>

            <div style={styles.curriculumResultsBox}>
              {curriculumLoading ? (
                <p style={styles.infoText}>Searching parsed PDFs...</p>
              ) : curriculumResults.length > 0 ? (
                curriculumResults.map((res, i) => (
                  <div key={i} style={styles.curriculumResultItem}>
                    • {res}
                  </div>
                ))
              ) : (
                <p style={styles.infoText}>Enter keywords to search the official syllabus PDF files.</p>
              )}
            </div>
          </div>
        </aside>

        {/* RIGHT COLUMN: AI CHAT TUTOR */}
        <main style={{
          ...styles.chatContainer,
          display: activeTab === 'chat' ? 'flex' : (window.innerWidth <= 768 ? 'none' : 'flex')
        }}>
          {subject && (
            <div style={styles.currentSubjectBanner}>
              Subject Context: <strong>{subject}</strong>
              <button onClick={() => setSubject('')} style={styles.clearSubjectBtn}>✕ Clear</button>
            </div>
          )}

          <div style={styles.chatBox}>
            {messages.length === 0 ? (
              <div style={styles.emptyChatPlaceholder}>
                <span style={styles.botLargeIcon}>🤖</span>
                <h3>Welcome to AcadeMate Assistant</h3>
                <p>Select a subject from the left panel to load its syllabus context, or ask a general KTU academic doubt below!</p>
                <div style={styles.suggestionChips}>
                  <button onClick={() => setInput("What is the time complexity of QuickSort?")} style={styles.chip}>QuickSort Complexity</button>
                  <button onClick={() => setInput("Explain circular linked lists")} style={styles.chip}>Circular Linked List</button>
                  <button onClick={() => setInput("What is Euler's Formula?")} style={styles.chip}>Euler's Formula</button>
                </div>
              </div>
            ) : (
              messages.map((msg, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2 }}
                  style={msg.sender === 'user' ? styles.userMsg : styles.botMsg}
                >
                  <div style={styles.messageContent}>{msg.text}</div>
                  {msg.aiGenerated && (
                    <span style={styles.aiTag}>
                      🤖 AI-Generated (Unverified)
                    </span>
                  )}
                </motion.div>
              ))
            )}
            {loading && (
              <div style={styles.loadingBubble}>
                <span style={styles.pulseDot}></span>
                <span style={styles.pulseDot}></span>
                <span style={styles.pulseDot}></span>
              </div>
            )}
          </div>

          <div style={styles.chatInputWrapper}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder={subject ? `Ask about ${subject}...` : "Ask your KTU academic doubt..."}
              style={styles.chatInput}
            />
            <button onClick={handleSend} style={styles.sendBtn} disabled={loading}>
              Send ⚡
            </button>
          </div>
        </main>
      </div>
    </div>
  );
};

/* THEME AND LAYOUT STYLING - FULLY PREMIUM & DYNAMIC */
const baseStyles = {
  appWrapper: {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
    overflow: 'hidden',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '12px 24px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
    zIndex: 10,
  },
  logoGroup: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  },
  logoIcon: {
    fontSize: '2rem',
  },
  headerTitle: {
    fontSize: '1.4rem',
    fontWeight: 'bold',
    margin: 0,
  },
  headerSubtitle: {
    fontSize: '0.8rem',
    margin: 0,
    opacity: 0.7,
  },
  userStatus: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
    fontSize: '0.9rem',
  },
  iconBtn: {
    background: 'transparent',
    border: '1px solid #ccc',
    padding: '6px 12px',
    borderRadius: '20px',
    cursor: 'pointer',
    fontSize: '0.8rem',
  },
  actionBtn: {
    background: '#0078ff',
    color: '#fff',
    border: 'none',
    padding: '6px 12px',
    borderRadius: '20px',
    cursor: 'pointer',
    fontSize: '0.8rem',
  },
  logoutBtn: {
    background: '#dc3545',
    color: '#fff',
    border: 'none',
    padding: '6px 12px',
    borderRadius: '20px',
    cursor: 'pointer',
    fontSize: '0.8rem',
  },
  mobileTabs: {
    display: 'none', // Overwritten in media queries or set to flex below
    width: '100%',
    borderBottom: '1px solid #ddd',
  },
  mobileTab: {
    flex: 1,
    padding: '12px',
    border: 'none',
    background: '#f8f9fa',
    cursor: 'pointer',
    textAlign: 'center',
    fontSize: '0.9rem',
    color: '#666',
  },
  activeMobileTab: {
    flex: 1,
    padding: '12px',
    border: 'none',
    borderBottom: '3px solid #0078ff',
    background: '#fff',
    fontWeight: 'bold',
    color: '#0078ff',
    cursor: 'pointer',
    textAlign: 'center',
    fontSize: '0.9rem',
  },
  mainContainer: {
    display: 'flex',
    flex: 1,
    overflow: 'hidden',
    position: 'relative',
  },
  sidebar: {
    width: '360px',
    flexDirection: 'column',
    padding: '16px',
    gap: '16px',
    overflowY: 'auto',
    borderRight: '1px solid #e0e0e0',
  },
  selectionCard: {
    padding: '14px',
    borderRadius: '8px',
    background: 'rgba(0,0,0,0.02)',
    border: '1px solid rgba(0,0,0,0.05)',
  },
  sectionHeading: {
    fontSize: '1rem',
    fontWeight: 'bold',
    margin: '0 0 12px 0',
  },
  selectorGroup: {
    display: 'flex',
    gap: '12px',
  },
  selectorField: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
  },
  label: {
    fontSize: '0.75rem',
    fontWeight: '600',
    opacity: 0.8,
  },
  select: {
    padding: '8px',
    borderRadius: '6px',
    border: '1px solid #ccc',
    outline: 'none',
    fontSize: '0.85rem',
    cursor: 'pointer',
  },
  academicCard: {
    padding: '14px',
    borderRadius: '8px',
    border: '1px solid rgba(0,0,0,0.08)',
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  subjectList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
    maxHeight: '200px',
    overflowY: 'auto',
  },
  subjectItem: {
    padding: '10px',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  subjectName: {
    fontSize: '0.85rem',
    fontWeight: '600',
  },
  subjectCode: {
    fontSize: '0.75rem',
    opacity: 0.6,
  },
  qpList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
    maxHeight: '260px',
    overflowY: 'auto',
  },
  qpItem: {
    padding: '10px',
    borderRadius: '6px',
    background: 'rgba(0,0,0,0.02)',
    border: '1px solid rgba(0,0,0,0.05)',
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
  },
  qpHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    fontSize: '0.8rem',
  },
  qpSubject: {
    fontWeight: 'bold',
  },
  qpYear: {
    opacity: 0.7,
  },
  qpQuestions: {
    margin: '4px 0',
    paddingLeft: '16px',
    fontSize: '0.75rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
  },
  qpQuestionText: {
    cursor: 'pointer',
    fontStyle: 'italic',
    padding: '2px',
    borderRadius: '4px',
  },
  downloadLink: {
    fontSize: '0.75rem',
    color: '#0078ff',
    textDecoration: 'none',
    fontWeight: 'bold',
    alignSelf: 'flex-start',
  },
  searchForm: {
    display: 'flex',
    gap: '8px',
  },
  searchBar: {
    flex: 1,
    padding: '8px 12px',
    borderRadius: '6px',
    border: '1px solid #ccc',
    fontSize: '0.85rem',
  },
  searchSubmit: {
    padding: '8px 12px',
    background: '#0078ff',
    color: '#fff',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '0.85rem',
  },
  curriculumResultsBox: {
    maxHeight: '150px',
    overflowY: 'auto',
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
  },
  curriculumResultItem: {
    fontSize: '0.75rem',
    lineHeight: 1.4,
    padding: '6px',
    borderRadius: '4px',
    background: 'rgba(0,0,0,0.02)',
  },
  chatContainer: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
  },
  currentSubjectBanner: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '8px 16px',
    background: 'rgba(0, 120, 255, 0.1)',
    fontSize: '0.85rem',
  },
  clearSubjectBtn: {
    background: 'transparent',
    border: 'none',
    color: '#dc3545',
    cursor: 'pointer',
    fontWeight: 'bold',
  },
  chatBox: {
    flex: 1,
    padding: '24px',
    overflowY: 'auto',
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
  },
  emptyChatPlaceholder: {
    margin: 'auto',
    textAlign: 'center',
    maxWidth: '480px',
    opacity: 0.8,
  },
  botLargeIcon: {
    fontSize: '3rem',
    display: 'block',
    marginBottom: '12px',
  },
  suggestionChips: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '8px',
    justifyContent: 'center',
    marginTop: '16px',
  },
  chip: {
    padding: '8px 12px',
    borderRadius: '20px',
    border: '1px solid #ccc',
    background: 'transparent',
    cursor: 'pointer',
    fontSize: '0.8rem',
  },
  userMsg: {
    alignSelf: 'flex-end',
    background: '#0078ff',
    color: '#fff',
    padding: '12px 18px',
    borderRadius: '18px 18px 2px 18px',
    maxWidth: '70%',
    boxShadow: '0 2px 5px rgba(0,120,255,0.2)',
  },
  botMsg: {
    alignSelf: 'flex-start',
    background: 'rgba(0,0,0,0.05)',
    color: '#333',
    padding: '12px 18px',
    borderRadius: '18px 18px 18px 2px',
    maxWidth: '70%',
    boxShadow: '0 2px 5px rgba(0,0,0,0.05)',
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
  },
  messageContent: {
    fontSize: '0.9rem',
    lineHeight: 1.4,
    whiteSpace: 'pre-wrap',
  },
  aiTag: {
    fontSize: '0.7rem',
    opacity: 0.6,
    fontStyle: 'italic',
    marginTop: '4px',
  },
  loadingBubble: {
    alignSelf: 'flex-start',
    padding: '12px 18px',
    borderRadius: '18px',
    background: 'rgba(0,0,0,0.05)',
    display: 'flex',
    gap: '4px',
    alignItems: 'center',
  },
  pulseDot: {
    width: '6px',
    height: '6px',
    borderRadius: '50%',
    background: '#666',
    animation: 'pulse 1.2s infinite ease-in-out',
  },
  chatInputWrapper: {
    display: 'flex',
    padding: '16px 24px',
    gap: '12px',
    alignItems: 'center',
  },
  chatInput: {
    flex: 1,
    padding: '12px 16px',
    borderRadius: '24px',
    border: '1px solid #ccc',
    fontSize: '0.9rem',
    outline: 'none',
  },
  sendBtn: {
    background: '#0078ff',
    color: '#fff',
    border: 'none',
    padding: '12px 24px',
    borderRadius: '24px',
    cursor: 'pointer',
    fontSize: '0.9rem',
    fontWeight: 'bold',
  },
  infoText: {
    fontSize: '0.8rem',
    opacity: 0.6,
    textAlign: 'center',
    margin: '12px 0',
  },
};

const lightStyles = {
  ...baseStyles,
  appWrapper: {
    ...baseStyles.appWrapper,
    background: '#f8f9fa',
    color: '#333',
  },
  header: {
    ...baseStyles.header,
    background: '#ffffff',
    borderBottom: '1px solid #e0e0e0',
  },
  sidebar: {
    ...baseStyles.sidebar,
    background: '#ffffff',
  },
  chatContainer: {
    ...baseStyles.chatContainer,
    background: '#f8f9fa',
  },
  botMsg: {
    ...baseStyles.botMsg,
    background: '#ffffff',
    color: '#333',
    border: '1px solid #e0e0e0',
  },
  chip: {
    ...baseStyles.chip,
    color: '#555',
    '&:hover': {
      background: '#eee',
    }
  }
};

const darkStyles = {
  ...baseStyles,
  appWrapper: {
    ...baseStyles.appWrapper,
    background: '#121212',
    color: '#f1f1f1',
  },
  header: {
    ...baseStyles.header,
    background: '#1e1e1e',
    borderBottom: '1px solid #2d2d2d',
  },
  iconBtn: {
    ...baseStyles.iconBtn,
    borderColor: '#444',
    color: '#f1f1f1',
  },
  sidebar: {
    ...baseStyles.sidebar,
    background: '#1e1e1e',
    borderRight: '1px solid #2d2d2d',
  },
  selectionCard: {
    ...baseStyles.selectionCard,
    background: 'rgba(255,255,255,0.02)',
    borderColor: 'rgba(255,255,255,0.05)',
  },
  select: {
    ...baseStyles.select,
    background: '#2d2d2d',
    color: '#f1f1f1',
    borderColor: '#444',
  },
  academicCard: {
    ...baseStyles.academicCard,
    borderColor: 'rgba(255,255,255,0.08)',
  },
  subjectItem: {
    ...baseStyles.subjectItem,
    color: '#ccc',
  },
  qpItem: {
    ...baseStyles.qpItem,
    background: 'rgba(255,255,255,0.02)',
    borderColor: 'rgba(255,255,255,0.05)',
  },
  searchBar: {
    ...baseStyles.searchBar,
    background: '#2d2d2d',
    color: '#f1f1f1',
    borderColor: '#444',
  },
  chatContainer: {
    ...baseStyles.chatContainer,
    background: '#121212',
  },
  chatBox: {
    ...baseStyles.chatBox,
    background: '#121212',
  },
  botMsg: {
    ...baseStyles.botMsg,
    background: '#1e1e1e',
    color: '#e0e0e0',
    boxShadow: 'none',
  },
  chip: {
    ...baseStyles.chip,
    color: '#ccc',
    borderColor: '#444',
  },
  chatInput: {
    ...baseStyles.chatInput,
    background: '#1e1e1e',
    color: '#f1f1f1',
    borderColor: '#2d2d2d',
  },
  curriculumResultItem: {
    ...baseStyles.curriculumResultItem,
    background: 'rgba(255,255,255,0.02)',
  },
};

export default Chatbot;
