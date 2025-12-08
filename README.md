# 🕌 Quran Search System - Hybrid Retrieval with LLM Explanations

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com)  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-336791)](https://www.postgresql.org)  
[![Qdrant](https://img.shields.io/badge/Vector%20DB-Qdrant-blueviolet)](https://qdrant.tech)  
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](https://www.docker.com)  
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)  

A production-ready Islamic search engine combining dense/sparse embeddings with Urdu LLM explanations. Search the Quran semantically and receive detailed explanations in Urdu.

---

## ✨ Features

- **🔍 Hybrid Search:** Combines semantic (dense) and keyword (sparse) embeddings  
- **🤖 Urdu LLM Explanations:** Detailed explanations in Urdu using open-source LLMs  
- **📊 Multi-vector Storage:** Separate Qdrant collections for optimized retrieval  
- **🌐 Ngrok Integration:** Easy external API access for Colab backend  
- **⚡ FastAPI Backend:** High-performance REST API with async support  
- **📈 Production Ready:** Comprehensive error handling, logging, and monitoring  
- **🔄 Graceful Fallbacks:** System continues working even if components fail  
- **🐘 PostgreSQL Integration:** Persistent verse storage and metadata management
- **🚀 Docker Support:** Containerized deployment for easy scaling

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Frontend                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │   FastAPI Backend Server       │
        │   (Port 8000)                  │
        └─┬──────┬──────────┬────────┬───┘
          │      │          │        │
          ▼      ▼          ▼        ▼
    ┌─────────┐ ┌──────────┐ ┌───────────┐ ┌──────────┐
    │ Qdrant  │ │PostgreSQL│ │LLM Service│ │Ngrok API │
    │Vector DB│ │Database  │ │(HF Models)│ │(Colab)   │
    └─────────┘ └──────────┘ └───────────┘ └──────────┘
         │            │            │             │
         └────────────┼────────────┴─────────────┘
                      │
                      ▼
          ┌──────────────────────┐
          │  Final Response      │
          │  (JSON with Results) │
          └──────────────────────┘
```

---

## 📁 Project Structure

```
quran_hadith_multilingual_rag/
├── README.md                          # Main documentation
├── requirements.txt                   # Project dependencies
├── docker-compose.yml                 # Multi-container orchestration
│
├── backend/                           # Backend service
│   ├── main.py                        # FastAPI entry point
│   ├── requirements.txt                # Backend dependencies
│   ├── .env.example                    # Environment template
│   ├── config/
│   │   └── settings.py                 # Configuration management
│   ├── api/
│   │   ├── routes.py                   # API endpoints
│   │   └── models.py                   # Request/response schemas
│   ├── services/
│   │   ├── qdrant_service.py           # Vector DB operations
│   │   ├── embedding_service.py        # Embedding generation
│   │   ├── postgres_service.py         # Database operations
│   │   ├── llm_service.py              # LLM explanation service
│   │   └── logger.py                   # Logging configuration
│   ├── scripts/
│   │   ├── setup_database.py           # PostgreSQL initialization
│   │   └── setup_qdrant.py             # Qdrant initialization
│   └── logs/
│       └── quran_search.log            # Application logs
│
├── frontend/                          # Frontend application
│   ├── index.html                      # Main page
│   ├── css/
│   │   └── style.css                   # Styling
│   ├── js/
│   │   └── app.js                      # Frontend logic
│   └── assets/                         # Images, icons
│
├── colab/                             # Google Colab notebooks
│   ├── embedding_service.ipynb         # Embedding generation
│   └── setup_instructions.md           # Setup guide
│
└── docs/                              # Additional documentation
    ├── API.md                          # API reference
    ├── SETUP.md                        # Detailed setup guide
    └── ARCHITECTURE.md                 # System architecture

```

---

## 🚀 Quick Start

### Prerequisites

```bash
✓ Python 3.9+
✓ PostgreSQL 14+
✓ Qdrant 1.9+ (or Docker)
✓ Redis (optional, for caching)
✓ Google Colab (for embeddings)
✓ Git
```

### Installation

**1. Clone Repository**

```bash
git clone https://github.com/yourusername/quran-search-system.git
cd quran-search-system
```

**2. Backend Setup**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env with your settings

python scripts/setup_database.py
python scripts/setup_qdrant.py
```

**3. Start Services**

```bash
# Terminal 1: PostgreSQL
sudo systemctl start postgresql

# Terminal 2: Qdrant (Docker)
docker run -p 6333:6333 qdrant/qdrant

# Terminal 3: Backend
python main.py
```

**4. Access Frontend**

Open `frontend/index.html` in your browser or:

```bash
# For development server
python -m http.server 8080 --directory frontend
```

Visit: `http://localhost:8080`

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=quran_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password_here

# Qdrant Vector Database
QDRANT_URL=http://localhost:6333
QDRANT_DENSE_COLLECTION=quran_dense
QDRANT_SPARSE_COLLECTION=quran_sparse

# Colab API (Embedding Service)
COLAB_API_URL=https://your-ngrok-url.ngrok-free.app
COLAB_TIMEOUT=30

# LLM Configuration
LLM_BASE_URL=https://api-inference.huggingface.co/models
LLM_MODEL=mistralai/Mistral-7B-Instruct-v0.2
HF_API_KEY=hf_your_api_key_here

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/quran_search.log

# Redis (Optional)
REDIS_HOST=localhost
REDIS_PORT=6379
CACHE_TTL=3600
```

---

## 🔌 API Endpoints

| Method | Endpoint                | Description                        |
|--------|-------------------------|-----------------------------------|
| POST   | `/search`               | Hybrid search with results         |
| POST   | `/detailed-explanation` | Get Urdu explanation for verses    |
| GET    | `/test-qdrant`          | Test Qdrant connection            |
| GET    | `/test-postgres`        | Test PostgreSQL connection        |
| GET    | `/test-colab`           | Test Colab embedding API          |
| GET    | `/health`               | System health status              |
| GET    | `/docs`                 | OpenAPI documentation (Swagger)   |

### Search API Example

**Request:**

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "نماز کی اہمیت",
    "top_k": 3,
    "language": "urdu"
  }'
```

**Response:**

```json
{
  "query": "نماز کی اہمیت",
  "top_results": [
    {
      "quran_id": 3486,
      "surah_id": 31,
      "ayah_id": 17,
      "score": 0.5999843,
      "arabic_text": "يَٰبُنَيَّ أَقِمِ ٱلصَّلَوٰةَ...",
      "urdu_text": "بیٹا، نماز قائم کرنے کا حکم دے...",
      "english_text": "O my son, establish prayer...",
      "surah_name_ur": "لقمان"
    }
  ],
  "llm_explanation": {
    "urdu": "تفصیلی وضاحت: نماز اسلام کا دوسرا رکن ہے...",
    "verses_used": [3486, 3385, 4269]
  },
  "execution_time": 2.345
}
```

---

## 🧪 Testing

**Connection Tests**

```bash
# Test all services
curl http://localhost:8000/health

# Test Qdrant
curl http://localhost:8000/test-qdrant

# Test PostgreSQL
curl http://localhost:8000/test-postgres

# Test Colab API
curl http://localhost:8000/test-colab
```

**Integration Test**

```python
import requests
import json

response = requests.post(
    "http://localhost:8000/search",
    json={"text": "نماز", "top_k": 2}
)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

---

## 🐛 Troubleshooting

### PostgreSQL Issues

```bash
# Check status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U postgres -d quran_db -c "SELECT COUNT(*) FROM verses;"

# View logs
sudo tail -f /var/log/postgresql/postgresql.log
```

### Qdrant Issues

```bash
# Check if running
curl http://localhost:6333

# View logs
docker logs <container_id>

# Restart
docker restart <container_id>
```

### API Connection Issues

```bash
# Check backend
curl http://localhost:8000/health

# View logs
tail -f backend/logs/quran_search.log

# Run with debug
export LOG_LEVEL=DEBUG
python backend/main.py
```

---

## 🐳 Docker Deployment

**Docker Compose (All Services)**

```bash
docker-compose up -d
```

**Build Backend Image**

```bash
cd backend
docker build -t quran-search-backend:latest .
docker run -p 8000:8000 quran-search-backend:latest
```

---

## 📚 Documentation

- **[Backend README](./backend/README.md)** - Detailed backend documentation
- **[API Reference](./docs/API.md)** - Complete API documentation
- **[Setup Guide](./docs/SETUP.md)** - Detailed installation instructions
- **[Architecture](./docs/ARCHITECTURE.md)** - System architecture details

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern async web framework
- **Qdrant** - Vector database for semantic search
- **PostgreSQL** - Reliable relational database
- **Hugging Face** - Open-source LLM models
- **Ngrok** - Secure tunneling service

<div align="center">

**Made with ❤️ for the Muslim Ummah**

If you find this project helpful, please consider giving it a ⭐

</div>