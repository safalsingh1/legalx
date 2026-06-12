"""
LegalX AI Knowledge Centre - Pipeline Orchestrator
Runs the full automated pipeline:
  scrape → AI process → vector index → audio generate → save JSON
"""

import asyncio
import json
import logging
import os

from pipeline.scraper import scrape_legal_content, get_all_topics
from pipeline.processor import generate_card_description, generate_summary, extract_key_info
from pipeline.vector_store import index_topic
from pipeline.audio import generate_audio, audio_exists

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CARDS_FILE = os.path.join(DATA_DIR, "cards.json")
TOPICS_FILE = os.path.join(DATA_DIR, "topics.json")


def save_card(topic_key: str, card_data: dict):
    """Save generated card data to JSON."""
    os.makedirs(DATA_DIR, exist_ok=True)
    cards = load_all_cards()
    cards[topic_key] = card_data
    with open(CARDS_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)


def load_all_cards() -> dict:
    """Load all generated cards from JSON."""
    if os.path.exists(CARDS_FILE):
        try:
            with open(CARDS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def load_card(topic_key: str) -> dict | None:
    """Load a single topic's card data."""
    return load_all_cards().get(topic_key)


async def process_topic(topic_key: str, topic_name: str, force: bool = False) -> dict:
    """
    Run the full pipeline for a single topic.
    Returns the generated card data.
    """
    existing = load_card(topic_key)
    if existing and not force:
        logger.info(f"[{topic_key}] Already processed, skipping (use force=True to reprocess)")
        return existing

    logger.info(f"[{topic_key}] Starting pipeline...")

    # Step 1: Scrape legal content
    logger.info(f"[{topic_key}] Step 1/5: Scraping legal content...")
    legal_text = await scrape_legal_content(topic_key)

    # Step 2: Generate card description
    logger.info(f"[{topic_key}] Step 2/5: Generating card description...")
    description = generate_card_description(topic_name, legal_text)

    # Step 3: Generate AI summary
    logger.info(f"[{topic_key}] Step 3/5: Generating AI summary...")
    summary = generate_summary(topic_name, legal_text)

    # Step 4: Extract key information
    logger.info(f"[{topic_key}] Step 4/5: Extracting key information...")
    key_info = extract_key_info(topic_name, legal_text)

    # Step 5: Index in ChromaDB for RAG
    logger.info(f"[{topic_key}] Step 5/5: Indexing in vector store...")
    chunk_count = index_topic(topic_key, legal_text, source_name=topic_name)

    # Step 6: Generate audio (async, non-blocking)
    logger.info(f"[{topic_key}] Bonus: Generating audio summary...")
    try:
        generate_audio(topic_key, summary)
        has_audio = True
    except Exception as e:
        logger.warning(f"[{topic_key}] Audio generation failed: {e}")
        has_audio = False

    card = {
        "key": topic_key,
        "name": topic_name,
        "description": description,
        "summary": summary,
        "key_info": key_info,
        "has_audio": has_audio,
        "chunk_count": chunk_count,
        "processed": True,
    }

    save_card(topic_key, card)
    logger.info(f"[{topic_key}] ✓ Pipeline complete!")
    return card


async def run_full_pipeline(force: bool = False):
    """
    Run the pipeline for all 5 legal topics sequentially.
    Called on server startup.
    """
    logger.info("=" * 60)
    logger.info("LegalX AI Pipeline Starting...")
    logger.info("=" * 60)

    topics = get_all_topics()
    results = {}

    for topic in topics:
        try:
            card = await process_topic(topic["key"], topic["name"], force=force)
            results[topic["key"]] = "success"
        except Exception as e:
            logger.error(f"[{topic['key']}] Pipeline failed: {e}", exc_info=True)
            results[topic["key"]] = f"error: {str(e)}"

    logger.info("=" * 60)
    logger.info(f"Pipeline complete. Results: {results}")
    logger.info("=" * 60)
    return results
