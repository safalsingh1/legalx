import { useState, useRef, useEffect } from 'react'
import { Play, Pause, Download, Volume2, VolumeX, Loader2 } from 'lucide-react'
import { API_BASE } from '../config'
import './AudioPlayer.css'

export default function AudioPlayer({ topicKey, topicName }) {
  const audioRef = useRef(null)
  const [playing, setPlaying] = useState(false)
  const [error, setError] = useState(null)
  const [progress, setProgress] = useState(0)
  const [duration, setDuration] = useState(0)
  const [muted, setMuted] = useState(false)
  const [volume, setVolume] = useState(1)

  const audioUrl = `${API_BASE}/api/topics/${topicKey}/audio`

  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause()
      }
    }
  }, [])

  const togglePlay = async () => {
    if (!audioRef.current) return
    setError(null)
    if (playing) {
      audioRef.current.pause()
    } else {
      try {
        await audioRef.current.play()
      } catch (e) {
        console.error("Playback error:", e)
        setError('Playback failed. Try again.')
      }
    }
  }

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setProgress((audioRef.current.currentTime / audioRef.current.duration) * 100 || 0)
    }
  }

  const handleLoadedMetadata = () => {
    if (audioRef.current) setDuration(audioRef.current.duration)
  }

  const handleSeek = (e) => {
    if (!audioRef.current || !audioRef.current.duration) return
    const rect = e.currentTarget.getBoundingClientRect()
    const x = e.clientX - rect.left
    const pct = x / rect.width
    audioRef.current.currentTime = pct * audioRef.current.duration
    setProgress(pct * 100)
  }

  const toggleMute = () => {
    if (audioRef.current) audioRef.current.muted = !muted
    setMuted(m => !m)
  }

  const formatTime = (s) => {
    if (!s || isNaN(s)) return '0:00'
    const m = Math.floor(s / 60)
    const sec = Math.floor(s % 60)
    return `${m}:${sec.toString().padStart(2, '0')}`
  }

  const currentTime = audioRef.current ? audioRef.current.currentTime : 0

  return (
    <div className="audio-player">
      <audio
        ref={audioRef}
        src={audioUrl}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onPlay={() => setPlaying(true)}
        onPause={() => setPlaying(false)}
        onEnded={() => { setPlaying(false); setProgress(0) }}
        onError={() => setError('Audio could not be loaded.')}
        preload="metadata"
      />

      <div className="audio-header">
        <div className="audio-icon-wrap">
          <Volume2 size={20} />
        </div>
        <div>
          <p className="audio-title">Audio Summary</p>
          <p className="audio-subtitle">{topicName}</p>
        </div>
      </div>

      {/* Waveform visualizer (decorative) */}
      <div className="waveform">
        {Array.from({ length: 40 }).map((_, i) => (
          <div
            key={i}
            className={`waveform-bar ${playing ? 'active' : ''}`}
            style={{
              height: `${20 + Math.sin(i * 0.8) * 15 + Math.random() * 10}px`,
              animationDelay: `${i * 50}ms`,
            }}
          />
        ))}
      </div>

      {/* Progress bar */}
      <div className="progress-wrap" onClick={handleSeek} id={`audio-progress-${topicKey}`}>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }} />
          <div className="progress-thumb" style={{ left: `${progress}%` }} />
        </div>
      </div>

      <div className="time-row">
        <span className="time">{formatTime(currentTime)}</span>
        <span className="time">{formatTime(duration)}</span>
      </div>

      {error && <p className="audio-error">{error}</p>}

      <div className="audio-controls">
        <button className="btn-icon" onClick={toggleMute} title={muted ? 'Unmute' : 'Mute'}>
          {muted ? <VolumeX size={16} /> : <Volume2 size={16} />}
        </button>

        <button
          className="play-btn"
          onClick={togglePlay}
          id={`play-btn-${topicKey}`}
        >
          {playing ? (
            <Pause size={22} />
          ) : (
            <Play size={22} style={{ marginLeft: '2px' }} />
          )}
        </button>

        <a
          href={audioUrl}
          download={`${topicKey}_summary.mp3`}
          className="btn-icon"
          title="Download MP3"
          id={`download-btn-${topicKey}`}
        >
          <Download size={16} />
        </a>
      </div>
    </div>
  )
}
