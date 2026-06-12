"""
LegalX AI Knowledge Centre - Groq AI Processing Pipeline
Uses Groq's LPU-accelerated inference (OpenAI-compatible API) for:
- Card description generation
- AI summary (≤250 words, plain English)
- Key information extraction (structured JSON)
- Legal Q&A answering
"""

import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Groq client - OpenAI-compatible, LPU-accelerated
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY", ""),
    base_url="https://api.groq.com/openai/v1",
)

# Model priority list — falls back automatically on 503 capacity errors
GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]


def _chat(system: str, user: str, temperature: float = 0.4, max_tokens: int = 1024) -> str:
    """Call Groq via OpenAI-compatible API with automatic model fallback on 503."""
    last_error = None
    for model in GROQ_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            if model != GROQ_MODELS[0]:
                logger.info(f"Used fallback model: {model}")
            return response.choices[0].message.content.strip()
        except Exception as e:
            err_str = str(e)
            if "503" in err_str or "over capacity" in err_str or "rate_limit" in err_str.lower():
                logger.warning(f"Model {model} unavailable: {err_str[:80]}. Trying next...")
                last_error = e
                continue
            raise  # re-raise non-capacity errors immediately
    raise RuntimeError(f"All Groq models failed. Last error: {last_error}")


def generate_card_description(topic_name: str, legal_text: str) -> str:
    """
    Generate a short 2-3 sentence card description for the homepage.
    """
    system = (
        "You are a legal content writer for LegalX, an Indian legal knowledge platform. "
        "Write concise, plain-English descriptions for legal topics so non-lawyers understand them immediately."
    )
    user = (
        f"Based on the following legal content about '{topic_name}', write a short 2-3 sentence "
        f"description suitable for a topic card on a knowledge centre homepage. "
        f"Keep it under 60 words. Make it accessible to common citizens.\n\n"
        f"Legal Content:\n{legal_text[:3000]}"
    )
    return _chat(system, user, temperature=0.5, max_tokens=250)


def generate_summary(topic_name: str, legal_text: str) -> str:
    """
    Generate a plain-English summary of the legal topic (max 250 words).
    """
    system = (
        "You are a legal simplifier for LegalX. Your job is to make Indian laws understandable "
        "to ordinary citizens with no legal background. Use simple language, short sentences, "
        "and avoid legal jargon wherever possible."
    )
    user = (
        f"Write a clear, easy-to-understand summary of '{topic_name}' based on the legal content below. "
        f"Requirements:\n"
        f"- Maximum 250 words\n"
        f"- Plain English, no legal jargon\n"
        f"- Suitable for an ordinary Indian citizen\n"
        f"- Mention what the law does, who it protects, and why it matters\n\n"
        f"Legal Content:\n{legal_text[:4000]}"
    )
    return _chat(system, user, temperature=0.4, max_tokens=800)


def extract_key_info(topic_name: str, legal_text: str) -> dict:
    """
    Extract structured key information from legal content.
    Returns: { key_rights, important_provisions, penalties, who_can_benefit }
    """
    system = (
        "You are a legal analyst for LegalX. Extract structured information from Indian legal texts. "
        "Always respond with valid JSON only, no markdown code blocks, no extra text."
    )
    user = (
        f"Extract key information from the following legal content about '{topic_name}'.\n"
        f"Return a JSON object with exactly these keys:\n"
        f"- 'key_rights': list of 4-6 key rights or entitlements (strings)\n"
        f"- 'important_provisions': list of 4-6 important legal provisions or sections (strings)\n"
        f"- 'penalties': list of 3-5 penalties for violations (strings)\n"
        f"- 'who_can_benefit': list of 3-5 categories of people/entities who benefit (strings)\n\n"
        f"Make each item a clear, concise sentence. Use plain English.\n\n"
        f"Legal Content:\n{legal_text[:4000]}"
    )
    raw = _chat(system, user, temperature=0.2, max_tokens=800)

    # Clean up in case model wraps in markdown
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip().rstrip("```").strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        logger.warning(f"JSON parse failed for key_info of {topic_name}, returning defaults")
        return {
            "key_rights": ["Information could not be extracted. Please try regenerating."],
            "important_provisions": [],
            "penalties": [],
            "who_can_benefit": [],
        }


def answer_question(topic_name: str, question: str, context_chunks: list[str]) -> str:
    """
    Answer a user question about a legal topic using retrieved RAG context.
    """
    context = "\n\n---\n\n".join(context_chunks) if context_chunks else ""
    system = (
        "You are LegalX AI Assistant, an expert in Indian law. "
        "Answer user questions clearly and accurately based on the provided legal context. "
        "Use plain language accessible to non-lawyers. "
        "If the answer is not in the context, say so honestly. "
        "Keep answers concise (under 200 words) unless the question requires detail."
    )
    user = (
        f"Topic: {topic_name}\n\n"
        f"Legal Context:\n{context}\n\n"
        f"User Question: {question}\n\n"
        f"Provide a helpful, accurate answer based on the context above."
    )
    return _chat(system, user, temperature=0.3, max_tokens=500)


def answer_question_no_rag(topic_name: str, question: str, legal_text: str) -> str:
    """
    Fallback: Answer question using full legal text (no RAG retrieval).
    """
    system = (
        "You are LegalX AI Assistant, an expert in Indian law. "
        "Answer user questions clearly and accurately. Use plain language."
    )
    user = (
        f"Based on this legal content about '{topic_name}':\n\n"
        f"{legal_text[:4000]}\n\n"
        f"Answer this question: {question}"
    )
    return _chat(system, user, temperature=0.3, max_tokens=500)
