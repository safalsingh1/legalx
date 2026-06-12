import { Shield, FileText, AlertTriangle, Users } from 'lucide-react'
import './KeyInfoPanel.css'

const SECTIONS = [
  {
    key: 'key_rights',
    label: 'Key Rights',
    icon: Shield,
    color: '#4f8ef7',
    bg: 'rgba(79,142,247,0.08)',
    border: 'rgba(79,142,247,0.2)',
  },
  {
    key: 'important_provisions',
    label: 'Important Provisions',
    icon: FileText,
    color: '#c9a84c',
    bg: 'rgba(201,168,76,0.08)',
    border: 'rgba(201,168,76,0.2)',
  },
  {
    key: 'penalties',
    label: 'Penalties',
    icon: AlertTriangle,
    color: '#ef4949',
    bg: 'rgba(239,73,73,0.08)',
    border: 'rgba(239,73,73,0.2)',
  },
  {
    key: 'who_can_benefit',
    label: 'Who Can Benefit',
    icon: Users,
    color: '#3ecf8e',
    bg: 'rgba(62,207,142,0.08)',
    border: 'rgba(62,207,142,0.2)',
  },
]

export default function KeyInfoPanel({ keyInfo }) {
  if (!keyInfo) return (
    <div className="key-info-empty">
      <div className="skeleton" style={{ height: '300px', borderRadius: 'var(--radius-lg)' }} />
    </div>
  )

  return (
    <div className="key-info-grid">
      {SECTIONS.map(({ key, label, icon: Icon, color, bg, border }) => {
        const items = keyInfo[key] || []
        return (
          <div
            key={key}
            className="key-info-card animate-fade-in-up"
            style={{ '--section-color': color, '--section-bg': bg, '--section-border': border }}
          >
            <div className="ki-header">
              <div className="ki-icon-wrap">
                <Icon size={16} />
              </div>
              <h4 className="ki-label">{label}</h4>
              <span className="ki-count">{items.length}</span>
            </div>
            <ul className="ki-list">
              {items.map((item, i) => (
                <li key={i} className="ki-item">
                  <span className="ki-bullet" />
                  <span>{item}</span>
                </li>
              ))}
              {items.length === 0 && (
                <li className="ki-empty">No information available</li>
              )}
            </ul>
          </div>
        )
      })}
    </div>
  )
}
