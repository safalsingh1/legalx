import { Link } from 'react-router-dom'
import { ArrowRight, Loader2, CheckCircle2, Volume2 } from 'lucide-react'
import './TopicCard.css'

const TOPIC_ICONS = {
  pocso: '🛡️',
  consumer_protection: '⚖️',
  cyber_crime: '🔐',
  rti: '📋',
  gst: '💼',
}

const TOPIC_COLORS = {
  pocso:              { accent: '#ef4949', glow: 'rgba(239,73,73,0.15)' },
  consumer_protection:{ accent: '#4f8ef7', glow: 'rgba(79,142,247,0.15)' },
  cyber_crime:        { accent: '#7c5cbf', glow: 'rgba(124,92,191,0.15)' },
  rti:                { accent: '#3ecf8e', glow: 'rgba(62,207,142,0.15)' },
  gst:                { accent: '#c9a84c', glow: 'rgba(201,168,76,0.15)' },
}

export default function TopicCard({ topic, index }) {
  const icon = TOPIC_ICONS[topic.key] || '📜'
  const colors = TOPIC_COLORS[topic.key] || { accent: '#c9a84c', glow: 'rgba(201,168,76,0.15)' }

  return (
    <article
      className="topic-card animate-fade-in-up"
      style={{
        animationDelay: `${index * 80}ms`,
        '--card-accent': colors.accent,
        '--card-glow': colors.glow,
      }}
    >
      <div className="card-glow-bg" />

      <div className="card-header">
        <div className="card-icon" style={{ background: colors.glow }}>
          <span className="card-emoji">{icon}</span>
        </div>
        <div className="card-badges">
          {topic.processed ? (
            <span className="badge badge-green">
              <CheckCircle2 size={10} /> AI Generated
            </span>
          ) : (
            <span className="badge badge-blue">
              <Loader2 size={10} className="spinning" /> Processing
            </span>
          )}
          {topic.has_audio && (
            <span className="badge badge-purple">
              <Volume2 size={10} /> Audio
            </span>
          )}
        </div>
      </div>

      <div className="card-body">
        <h3 className="card-title">{topic.name}</h3>
        <p className="card-full-name">{topic.full_name}</p>
        <p className="card-description">
          {topic.processed
            ? topic.description
            : 'AI is generating content for this topic. Please refresh in a moment...'}
        </p>
      </div>

      <div className="card-footer">
        <Link to={`/topic/${topic.key}`} className="btn btn-primary card-cta">
          Read More <ArrowRight size={15} />
        </Link>
      </div>
    </article>
  )
}
