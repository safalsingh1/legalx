import { Link, useLocation } from 'react-router-dom'
import { Scale, Zap } from 'lucide-react'
import './Navbar.css'

export default function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-logo">
          <div className="logo-icon">
            <Scale size={18} strokeWidth={2.5} />
          </div>
          <span className="logo-text">
            Legal<span className="text-gold">X</span>
          </span>
          <span className="logo-badge">
            <Zap size={10} />
            AI
          </span>
        </Link>

        <div className="navbar-center hide-mobile">
          <span className="navbar-tagline">AI-Powered Legal Knowledge Centre</span>
        </div>

        <div className="navbar-right">
          <a
            href="https://console.groq.com"
            target="_blank"
            rel="noreferrer"
            className="btn btn-ghost"
            style={{ fontSize: '0.8rem', padding: '7px 14px' }}
          >
            Powered by Groq
          </a>
        </div>
      </div>
    </nav>
  )
}
