"""
LegalX AI Knowledge Centre - Audio Generation
Converts AI-generated summaries to speech using gTTS (Google Text-to-Speech).
Saves MP3 files to the audio/ directory and serves them via FastAPI.
"""

import os
import logging
from gtts import gTTS

logger = logging.getLogger(__name__)

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "audio")


def generate_audio(topic_key: str, summary_text: str) -> str:
    """
    Convert summary text to MP3 audio using gTTS.
    Returns the filename of the generated audio file.
    """
    os.makedirs(AUDIO_DIR, exist_ok=True)
    filename = f"{topic_key}_summary.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    try:
        tts = gTTS(text=summary_text, lang="en", tld="co.in", slow=False)
        tts.save(filepath)
        logger.info(f"Audio generated: {filepath}")
        return filename
    except Exception as e:
        logger.error(f"Audio generation failed for {topic_key}: {e}")
        raise


def audio_exists(topic_key: str) -> bool:
    """Check if audio file already exists for a topic."""
    filepath = os.path.join(AUDIO_DIR, f"{topic_key}_summary.mp3")
    return os.path.exists(filepath)


def get_audio_path(topic_key: str) -> str | None:
    """Return full path to audio file if it exists."""
    filepath = os.path.join(AUDIO_DIR, f"{topic_key}_summary.mp3")
    return filepath if os.path.exists(filepath) else None
