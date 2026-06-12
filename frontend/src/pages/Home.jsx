import { useState, useEffect } from 'react'
import { RefreshCw, Loader2, Scale, Sparkles, Shield, BookOpen } from 'lucide-react'
import TopicCard from '../components/TopicCard'
import { API_BASE } from '../config'
import './Home.css'

const STATS = [
  { icon: Scale, label: 'Legal Topics', value: '5' },
  { icon: Sparkles, label: 'AI Generated', value: '100%' },
  { icon: Shield, label: 'Verified Laws', value: 'GOI' },
  { icon: BookOpen, label: 'Powered By', value: 'Groq' },
]

const STATIC_TOPICS = [
  { key: 'pocso',               name: 'POCSO Act',                    full_name: 'Protection of Children from Sexual Offences Act, 2012', processed: false, has_audio: false, description: '' },
  { key: 'consumer_protection', name: 'Consumer Protection Act',       full_name: 'Consumer Protection Act, 2019',                         processed: false, has_audio: false, description: '' },
  { key: 'cyber_crime',         name: 'Cyber Crime Laws',              full_name: 'Information Technology Act, 2000 & Cyber Crime Laws',    processed: false, has_audio: false, description: '' },
  { key: 'rti',                 name: 'Right to Information (RTI) Act',full_name: 'Right to Information Act, 2005',                        processed: false, has_audio: false, description: '' },
  { key: 'gst',                 name: 'GST Registration',              full_name: 'Goods and Services Tax (GST) Registration & Law',        processed: false, has_audio: false, description: '' },
]

export default function Home() {
  const [topics, setTopics] = useState(STATIC_TOPICS)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [refreshing, setRefreshing] = useState(false)

  const fetchTopics = async (showLoader = false) => {
    if (showLoader) setRefreshing(true)
    try {
      const res = await fetch(`${API_BASE}/api/topics`)
      if (!res.ok) throw new Error('Failed to fetch topics')
      const data = await res.json()
      setTopics(data)
      setError(null)
    } catch (err) {
      // Keep static topics visible on error — just show a subtle notice
      setError(err.message)
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }

  useEffect(() => {
    fetchTopics()
    const interval = setInterval(() => {
      fetchTopics()
    }, 10000)
    return () => clearInterval(interval)
  }, [])

  const allProcessed = topics.length > 0 && topics.every(t => t.processed)


  return (
    <main className="home-page">
      {/* Hero */}
      <section className="hero">
        <div className="hero-inner">
          <div className="hero-badge animate-fade-in">
            <Sparkles size={12} />
            AI-Powered Legal Knowledge
          </div>
          <h1 className="hero-title animate-fade-in-up">
            Understand Indian Laws
            <br />
            <span className="text-gold">Made Simple</span>
          </h1>
          <p className="hero-subtitle animate-fade-in-up" style={{ animationDelay: '100ms' }}>
            LegalX uses Groq AI to automatically process legal texts and generate plain-English
            summaries, key insights, and intelligent Q&A — so every citizen can understand
            their rights.
          </p>

          {/* Stats */}
          <div className="hero-stats animate-fade-in-up" style={{ animationDelay: '200ms' }}>
            {STATS.map(({ icon: Icon, label, value }) => (
              <div key={label} className="stat-item">
                <div className="stat-icon"><Icon size={14} /></div>
                <div>
                  <p className="stat-value">{value}</p>
                  <p className="stat-label">{label}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="hero-glow" />
      </section>

      {/* Pipeline status banner — show whenever any topic unprocessed */}
      {!allProcessed && topics.length > 0 && (
        <div className="pipeline-banner">
          <Loader2 size={16} className="spinning" />
          <span>
            Groq AI pipeline is processing legal content. Topics will auto-update every 10 seconds.
          </span>
        </div>
      )}

      {/* Topics section */}
      <section className="topics-section">
        <div className="section-header">
          <div>
            <p className="section-title">Knowledge Centre</p>
            <h2 className="section-heading">Legal Topics</h2>
          </div>
          <button
            className="btn btn-ghost"
            onClick={() => fetchTopics(true)}
            disabled={refreshing}
            id="refresh-topics-btn"
          >
            <RefreshCw size={15} className={refreshing ? 'spinning' : ''} />
            Refresh
          </button>
        </div>

        {error && (
          <div className="error-state" style={{ marginBottom: 'var(--space-md)' }}>
            <p style={{ fontSize: '0.82rem' }}>⚠️ Could not reach backend: {error}</p>
            <button className="btn btn-ghost" onClick={() => fetchTopics()}>Retry</button>
          </div>
        )}

        <div className="topics-grid">
          {topics.map((topic, i) => (
            <TopicCard key={topic.key} topic={topic} index={i} />
          ))}
        </div>
      </section>


      {/* Footer */}
      <footer className="home-footer">
        <p>
          Built for <strong>LegalX AI/ML Internship — Round 2</strong>.
          Powered by <span className="text-gold">Groq (LLaMA 3.3 70B)</span> + ChromaDB RAG + gTTS.
        </p>
      </footer>
    </main>
  )
}
