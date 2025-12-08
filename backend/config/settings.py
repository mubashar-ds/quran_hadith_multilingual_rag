# Qdrant Configuration
import os

QDRANT_URL = "http://localhost:6333"
QDRANT_DENSE_COLLECTION = "quran_dense"
QDRANT_SPARSE_COLLECTION = "quran_sparse"

# PostgreSQL Configuration
POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "islamic_search",
    "user": "abdul",
    "password": "abd"
}

# LLM Configuration (HuggingFace)
HF_TOKEN = os.getenv("HF_TOKEN")
LLM_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
LLM_BASE_URL = "https://api-inference.huggingface.co/v1/"

# Embedding Service (Google Colab)
COLAB_API_URL = "https://pseudoclerically-nonlisting-kimberley.ngrok-free.dev"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "logs/quran_search.log"