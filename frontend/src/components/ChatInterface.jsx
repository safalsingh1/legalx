import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Loader2, BookOpen, Zap, RotateCcw } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { API_BASE } from '../config'
import './ChatInterface.css'

const EXAMPLE_QUESTIONS = {
  pocso: ['What is the punishment under POCSO?', 'Who must report a POCSO offence?', 'What rights does a child victim have?'],
  consumer_protection: ['What are my rights as a consumer?', 'How do I file a consumer complaint?', 'What is the compensation limit?'],
  cyber_crime: ['What is cyber fraud and its punishment?', 'How do I report a cybercrime?', 'What is identity theft under IT Act?'],
  rti: ['Who can file an RTI request?', 'What is the time limit to get a response?', 'What information is exempt from RTI?'],
  gst: ['When is GST registration mandatory?', 'What are the GST tax slabs?', 'What is Input Tax Credit?'],
}

function Message({ msg }) {
  const isUser = msg.role === 'user'
  return (
    <div className={`chat-msg ${isUser ? 'user' : 'assistant'}`}>
      <div className="msg-avatar">
        {isUser ? <User size={14} /> : <Bot size={14} />}
      </div>
      <div className="msg-content">
        <div className="msg-text">
          <ReactMarkdown>{msg.content}</ReactMarkdown>
        </div>
        {msg.sources && msg.sources.length > 0 && (
          <div className="msg-sources">
            <span className="sources-label"><BookOpen size={11} /> Sources ({msg.method})</span>
            {msg.sources.slice(0, 3).map((s, i) => (
              <div key={i} className="source-chip">
                <span className="source-score">{Math.round(s.score * 100)}%</span>
                <span className="source-text">{s.text}</span>
              </div>
            ))}
          </div>
        )}
        {msg.method && (
          <span className={`msg-method-badge ${msg.method === 'RAG' ? 'rag' : 'direct'}`}>
            <Zap size={9} /> {msg.method === 'RAG' ? 'RAG Retrieval' : 'Direct LLM'}
          </span>
        )}
      </div>
    </div>
  )
}

export default function ChatInterface({ topicKey, topicName }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `Hello! I'm your LegalX AI Assistant. I'm powered by Grok and can answer questions about ${topicName}. What would you like to know?`,
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)
  const inputRef = useRef(null)

  const examples = EXAMPLE_QUESTIONS[topicKey] || []

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (question) => {
    const q = (question || input).trim()
    if (!q || loading) return

    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: q }])
    setLoading(true)

    try {
      const res = await fetch(`${API_BASE}/api/topics/${topicKey}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Failed to get answer')

      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: data.answer,
          sources: data.sources,
          method: data.method,
        },
      ])
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: `Sorry, I couldn't process that. Error: ${err.message}` },
      ])
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage() }
  }

  const clearChat = () => {
    setMessages([{
      role: 'assistant',
      content: `Hello! I'm your LegalX AI Assistant powered by Grok. Ask me anything about ${topicName}.`,
    }])
  }

  return (
    <div className="chat-container">
      {/* Example questions */}
      {messages.length <= 1 && (
        <div className="chat-examples">
          <p className="examples-label">Try asking:</p>
          <div className="examples-list">
            {examples.map((q, i) => (
              <button key={i} className="example-chip" onClick={() => sendMessage(q)}>
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="chat-messages">
        {messages.map((msg, i) => <Message key={i} msg={msg} />)}
        {loading && (
          <div className="chat-msg assistant">
            <div className="msg-avatar"><Bot size={14} /></div>
            <div className="msg-content">
              <div className="typing-indicator">
                <span /><span /><span />
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <div className="chat-input-bar">
        <button className="btn-icon" onClick={clearChat} title="Clear chat">
          <RotateCcw size={15} />
        </button>
        <textarea
          ref={inputRef}
          className="input chat-input"
          placeholder={`Ask about ${topicName}...`}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          id={`chat-input-${topicKey}`}
        />
        <button
          className="btn btn-primary send-btn"
          onClick={() => sendMessage()}
          disabled={!input.trim() || loading}
          id={`send-btn-${topicKey}`}
        >
          {loading ? <Loader2 size={16} className="spinning" /> : <Send size={16} />}
        </button>
      </div>
    </div>
  )
}
