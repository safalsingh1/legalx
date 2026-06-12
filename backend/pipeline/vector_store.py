"""
LegalX AI Knowledge Centre - ChromaDB Vector Store for RAG
Uses sentence-transformers for local embeddings (no external API needed).
Each legal topic gets its own ChromaDB collection for isolated retrieval.
Compatible with ChromaDB 0.6.x and NumPy 2.x.
"""

import os
import logging
import chromadb

logger = logging.getLogger(__name__)

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
CHUNK_SIZE = 500       # characters per chunk
CHUNK_OVERLAP = 100    # overlap between chunks

# Lazy-load embedding function — avoids blocking startup with model download
_ef = None
_client = None


def _get_ef():
    """Lazy-initialize the sentence-transformers embedding function."""
    global _ef
    if _ef is None:
        from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
        _ef = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        logger.info("SentenceTransformer embedding function initialized.")
    return _ef


def _get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        os.makedirs(CHROMA_DIR, exist_ok=True)
        _client = chromadb.PersistentClient(path=CHROMA_DIR)
    return _client


def _chunk_text(text: str) -> list[str]:
    """Split text into overlapping chunks for better retrieval."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk = text[start:end].strip()
        if len(chunk) > 50:  # skip tiny chunks
            chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def index_topic(topic_key: str, legal_text: str, source_name: str = "") -> int:
    """
    Index legal text chunks into ChromaDB for a topic.
    Returns number of chunks indexed.
    """
    client = _get_client()
    ef = _get_ef()
    collection_name = f"legal_{topic_key}"

    # Delete existing collection to re-index
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    collection = client.create_collection(
        name=collection_name,
        embedding_function=ef,
        metadata={"topic": topic_key},
    )

    chunks = _chunk_text(legal_text)
    if not chunks:
        logger.warning(f"No chunks generated for {topic_key}")
        return 0

    ids = [f"{topic_key}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source_name, "chunk_index": i} for i in range(len(chunks))]

    collection.add(documents=chunks, ids=ids, metadatas=metadatas)
    logger.info(f"Indexed {len(chunks)} chunks for {topic_key}")
    return len(chunks)


def retrieve_context(topic_key: str, query: str, n_results: int = 4) -> list[dict]:
    """
    Retrieve the most relevant chunks for a query from a topic's collection.
    Returns list of { text, source, score } dicts.
    """
    client = _get_client()
    ef = _get_ef()
    collection_name = f"legal_{topic_key}"

    try:
        collection = client.get_collection(
            name=collection_name,
            embedding_function=ef,
        )
    except Exception:
        logger.warning(f"Collection {collection_name} not found, returning empty context")
        return []

    count = collection.count()
    if count == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, count),
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    if results and results["documents"]:
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            chunks.append({
                "text": doc,
                "source": meta.get("source", "Legal Database"),
                "score": round(max(0.0, 1 - dist), 3),  # convert distance to similarity
            })
    return chunks


def is_topic_indexed(topic_key: str) -> bool:
    """Check if a topic has been indexed in ChromaDB."""
    client = _get_client()
    ef = _get_ef()
    try:
        col = client.get_collection(f"legal_{topic_key}", embedding_function=ef)
        return col.count() > 0
    except Exception:
        return False
