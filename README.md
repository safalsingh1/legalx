# ⚖️ LegalX AI Knowledge Centre

> **LegalX AI/ML Internship — Round 2 Assessment Submission**

An AI-powered Legal Knowledge Centre that automatically processes Indian legal texts using **Grok (xAI)** and presents them through a beautiful, modern web interface.

---

## 🚀 Live Features

| Feature | Status | Description |
|---------|--------|-------------|
| 🗂️ Knowledge Cards | ✅ | Auto-generated from legal texts via Grok |
| 📝 AI Summary | ✅ | ≤250 word plain-English summaries |
| 🔑 Key Info Extraction | ✅ | Rights, provisions, penalties, beneficiaries |
| 🤖 AI Legal Assistant | ✅ | RAG-powered Q&A with Grok |
| 🔊 Audio Summary | ✅ | gTTS MP3 + download |
| 🔍 Source Citations | ✅ | RAG chunks with relevance scores |
| 💾 Chat History | ✅ | Per-session message history |
| 🗃️ Vector DB (RAG) | ✅ | ChromaDB with sentence-transformers |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)               │
│  Home (5 topic cards) → TopicDetail (4 tabs)            │
│  Summary | Key Info | Ask AI (chat) | Audio Player      │
└────────────────────┬────────────────────────────────────┘
                     │ REST API (/api/*)
┌────────────────────▼────────────────────────────────────┐
│                   Backend (FastAPI)                      │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │            AI Processing Pipeline                 │   │
│  │                                                   │   │
│  │  1. scraper.py  → Fetch legal text               │   │
│  │        ↓                                         │   │
│  │  2. processor.py → Grok AI (xAI API)             │   │
│  │     • generate_card_description()                │   │
│  │     • generate_summary() [≤250 words]            │   │
│  │     • extract_key_info() [structured JSON]       │   │
│  │        ↓                                         │   │
│  │  3. vector_store.py → ChromaDB                   │   │
│  │     • Chunk legal text (500 chars, 100 overlap)  │   │
│  │     • Embed with sentence-transformers           │   │
│  │     • Persist per-topic collection               │   │
│  │        ↓                                         │   │
│  │  4. audio.py → gTTS MP3 generation               │   │
│  │        ↓                                         │   │
│  │  5. Save to data/cards.json                      │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  Q&A Flow: Query → ChromaDB retrieval → Grok generation │
└─────────────────────────────────────────────────────────┘
```

---

## 🤖 AI Models Used

| Purpose | Model/Service |
|---------|--------------|
| Summarization | `grok-3-mini` via xAI API |
| Key Info Extraction | `grok-3-mini` via xAI API |
| Card Description | `grok-3-mini` via xAI API |
| Q&A (RAG) | `grok-3-mini` via xAI API |
| Embeddings | `all-MiniLM-L6-v2` (sentence-transformers, local) |
| Audio TTS | Google Text-to-Speech (gTTS) |
| Vector DB | ChromaDB (persisted) |

---

## 🛠️ Tech Stack

**Backend**
- Python 3.11+
- FastAPI + Uvicorn
- openai SDK (pointed at `api.x.ai/v1` for Grok)
- ChromaDB (vector store)
- sentence-transformers (local embeddings)
- gTTS (audio)
- httpx + BeautifulSoup4 (scraping)

**Frontend**
- React 18 + Vite
- React Router v6
- Vanilla CSS (glassmorphism dark theme)
- lucide-react (icons)

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- A **Grok API key** from [console.x.ai](https://console.x.ai)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure API key
copy .env.example .env
# Edit .env and set: XAI_API_KEY=your_key_here

# Start server
uvicorn main:app --reload --port 8000
```

The pipeline runs **automatically on startup** — it will:
1. Scrape legal content for all 5 topics
2. Generate summaries, descriptions, and key info via Grok
3. Index text in ChromaDB for RAG
4. Generate MP3 audio files

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

---

## 📋 Legal Topics Covered

1. **POCSO Act** — Protection of Children from Sexual Offences Act, 2012
2. **Consumer Protection Act** — Consumer Protection Act, 2019
3. **Cyber Crime Laws** — IT Act 2000 + BNS 2023
4. **RTI Act** — Right to Information Act, 2005
5. **GST Registration** — Goods and Services Tax Law

---

## 🔄 Automation Pipeline

The system is **fully automated** — no manual content writing:

```
Legal Source Text (govt/public domain)
        ↓
[Grok AI] → Card Description (2-3 sentences)
        ↓
[Grok AI] → Summary (≤250 words, plain English)
        ↓
[Grok AI] → Key Info (JSON: rights, provisions, penalties, beneficiaries)
        ↓
[sentence-transformers] → Text embeddings
        ↓
[ChromaDB] → Vector store (per-topic collection)
        ↓
[gTTS] → MP3 audio
        ↓
[JSON store] → Cached for fast retrieval
```

**Q&A RAG Flow:**
```
User question → ChromaDB similarity search → Top-4 chunks retrieved
        ↓
[Grok] → Answer grounded in retrieved legal text + source citations
```

---

## 🎯 Challenges Faced

1. **xAI API rate limits** — Used `grok-3-mini` for cost efficiency; sequential processing avoids hammering limits
2. **Structured JSON from LLM** — Added robust JSON parsing with markdown code block stripping
3. **Embedding model cold start** — `all-MiniLM-L6-v2` downloads on first run (~90MB), subsequent runs are instant
4. **Audio generation** — gTTS requires internet; falls back gracefully if offline

---

## 🔮 Future Improvements

- [ ] Multi-language support (Hindi, Tamil, Bengali)
- [ ] Semantic search across all topics
- [ ] User authentication + saved Q&A history
- [ ] Streaming responses from Grok (SSE)
- [ ] Upload custom legal documents for processing
- [ ] Dockerization + cloud deployment
- [ ] Speech-to-text input for questions
- [ ] Weekly auto-refresh of legal content

---

## 📁 Project Structure

```
legalX/
├── backend/
│   ├── main.py                  # FastAPI app
│   ├── requirements.txt
│   ├── .env.example
│   ├── pipeline/
│   │   ├── scraper.py           # Legal content fetcher
│   │   ├── processor.py         # Grok AI processing
│   │   ├── vector_store.py      # ChromaDB RAG
│   │   ├── audio.py             # gTTS audio generation
│   │   └── run_pipeline.py      # Pipeline orchestrator
│   ├── data/                    # Generated JSON + ChromaDB
│   └── audio/                   # Generated MP3 files
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Home.jsx          # Knowledge Centre homepage
    │   │   └── TopicDetail.jsx   # Topic detail with 4 tabs
    │   ├── components/
    │   │   ├── Navbar.jsx
    │   │   ├── TopicCard.jsx
    │   │   ├── KeyInfoPanel.jsx
    │   │   ├── ChatInterface.jsx  # AI chat with RAG
    │   │   └── AudioPlayer.jsx
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css             # Design system
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

*Built with ❤️ for LegalX AI/ML Internship Round 2 · Powered by Grok (xAI)*
