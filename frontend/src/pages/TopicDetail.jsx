import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  ArrowLeft, FileText, Info, MessageSquare, Volume2,
  Loader2, RefreshCw, AlertCircle, CheckCircle2, Zap
} from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { API_BASE } from '../config'
import KeyInfoPanel from '../components/KeyInfoPanel'
import ChatInterface from '../components/ChatInterface'
import AudioPlayer from '../components/AudioPlayer'
import './TopicDetail.css'

const TABS = [
  { id: 'summary',  label: 'Summary',       icon: FileText },
  { id: 'keyinfo',  label: 'Key Info',       icon: Info },
  { id: 'ask',      label: 'Ask AI',         icon: MessageSquare },
  { id: 'audio',    label: 'Audio Summary',  icon: Volume2 },
]

const TOPIC_ICONS = {
  pocso: '🛡️',
  consumer_protection: '⚖️',
  cyber_crime: '🔐',
  rti: '📋',
  gst: '💼',
}

export default function TopicDetail() {
  const { key } = useParams()
  const [topic, setTopic] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('summary')
  const [regenerating, setRegenerating] = useState(false)
  const [toast, setToast] = useState(null)

  const fetchTopic = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/topics/${key}`)
      if (!res.ok) throw new Error('Topic not found')
      const data = await res.json()
      setTopic(data)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTopic()
    const interval = setInterval(fetchTopic, 20000)
    return () => clearInterval(interval)
  }, [key])

  const handleRegenerate = async () => {
    setRegenerating(true)
    try {
      const res = await fetch(`${API_BASE}/api/topics/${key}/regenerate`, { method: 'POST' })
      const data = await res.json()
      showToast(data.message || 'Re-processing started...')
    } catch {
      showToast('Failed to trigger regeneration.')
    } finally {
      setRegenerating(false)
    }
  }

  const showToast = (msg) => {
    setToast(msg)
    setTimeout(() => setToast(null), 4000)
  }

  const wordCount = (text) => text?.split(/\s+/).filter(Boolean).length || 0

  if (loading) return (
    <div className="topic-detail-loading">
      <div className="loading-spinner">
        <Loader2 size={32} className="spinning" />
        <p>Loading legal content...</p>
      </div>
    </div>
  )

  if (error) return (
    <div className="topic-detail-error">
      <AlertCircle size={40} color="var(--accent-red)" />
      <p>{error}</p>
      <Link to="/" className="btn btn-ghost"><ArrowLeft size={15} /> Back to Home</Link>
    </div>
  )

  const icon = TOPIC_ICONS[key] || '📜'

  return (
    <div className="topic-detail">
      {/* Back bar */}
      <div className="detail-topbar">
        <div className="detail-topbar-inner">
          <Link to="/" className="btn btn-ghost back-btn">
            <ArrowLeft size={15} /> Knowledge Centre
          </Link>
          <div className="detail-actions">
            <button
              className="btn btn-ghost"
              onClick={handleRegenerate}
              disabled={regenerating}
              id={`regen-btn-${key}`}
            >
              <RefreshCw size={14} className={regenerating ? 'spinning' : ''} />
              <span className="hide-mobile">Regenerate</span>
            </button>
          </div>
        </div>
      </div>

      <div className="detail-container">
        {/* Header */}
        <header className="detail-header animate-fade-in-up">
          <div className="detail-topic-icon">{icon}</div>
          <div>
            <div className="detail-badges">
              {topic.processed ? (
                <span className="badge badge-green"><CheckCircle2 size={10} /> AI Generated</span>
              ) : (
                <span className="badge badge-blue"><Loader2 size={10} className="spinning" /> Processing</span>
              )}
              <span className="badge badge-gold"><Zap size={10} /> Groq Powered</span>
              {topic.has_audio && <span className="badge badge-purple"><Volume2 size={10} /> Audio Ready</span>}
            </div>
            <h1 className="detail-title">{topic.name}</h1>
            <p className="detail-full-name">{topic.full_name}</p>
          </div>
        </header>

        {/* Tabs */}
        <div className="tabs detail-tabs animate-fade-in" style={{ animationDelay: '100ms' }}>
          {TABS.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              className={`tab-btn ${activeTab === id ? 'active' : ''}`}
              onClick={() => setActiveTab(id)}
              id={`tab-${id}`}
            >
              <Icon size={14} />
              {label}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="detail-content animate-fade-in" key={activeTab}>

          {/* SUMMARY TAB */}
          {activeTab === 'summary' && (
            <div className="summary-panel glass-card" style={{ padding: 'var(--space-xl)' }}>
              <div className="summary-header">
                <div>
                  <h2 className="panel-title">AI Summary</h2>
                  <p className="panel-subtitle">Simplified for every citizen · {wordCount(topic.summary)} words</p>
                </div>
                {topic.summary && (
                  <span className="badge badge-gold">≤ 250 words</span>
                )}
              </div>
              <div className="divider" />
              {topic.summary ? (
                <div className="summary-markdown">
                  <ReactMarkdown>{topic.summary}</ReactMarkdown>
                </div>
              ) : (
                <div className="processing-state">
                  <Loader2 size={24} className="spinning" color="var(--gold)" />
                  <p>Groq is generating a plain-English summary. This takes about 15–30 seconds...</p>
                </div>
              )}
            </div>
          )}

          {/* KEY INFO TAB */}
          {activeTab === 'keyinfo' && (
            <div>
              <div className="panel-header-row">
                <h2 className="panel-title">Key Information</h2>
                <p className="panel-subtitle">Extracted by Groq AI from official legal texts</p>
              </div>
              <div className="divider" />
              <KeyInfoPanel keyInfo={topic.key_info} />
            </div>
          )}

          {/* ASK AI TAB */}
          {activeTab === 'ask' && (
            <div>
              <div className="panel-header-row">
                <div>
                  <h2 className="panel-title">AI Legal Assistant</h2>
                  <p className="panel-subtitle">
                    Powered by Groq + RAG (ChromaDB) · Ask anything about {topic.name}
                  </p>
                </div>
                <div className="rag-badge">
                  <span className="badge badge-green">RAG Enabled</span>
                </div>
              </div>
              <div className="divider" />
              <ChatInterface topicKey={key} topicName={topic.name} />
            </div>
          )}

          {/* AUDIO TAB */}
          {activeTab === 'audio' && (
            <div className="audio-tab-content">
              <div className="panel-header-row">
                <div>
                  <h2 className="panel-title">Audio Summary</h2>
                  <p className="panel-subtitle">Listen to the AI-generated summary · gTTS powered</p>
                </div>
              </div>
              <div className="divider" />
              <AudioPlayer topicKey={key} topicName={topic.name} />
              <div className="audio-note">
                <Info size={14} />
                <span>Audio is auto-generated from the AI summary using Google Text-to-Speech (Indian English accent).</span>
              </div>
            </div>
          )}

        </div>
      </div>

      {/* Toast */}
      {toast && <div className="toast">{toast}</div>}
    </div>
  )
}
