# Qdrant Configuration
QDRANT_URL = "http://localhost:6333"
QDRANT_DENSE_COLLECTION = "quran_dense"
QDRANT_SPARSE_COLLECTION = "quran_sparse"

# PostgreSQL Configuration
POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "islamic_search",
    "user": "abdul",
    "password": ""
}

# LLM Configuration (HuggingFace)
HF_TOKEN = ""  # Your working token
LLM_MODEL = "moonshotai/Kimi-K2-Instruct-0905"     # The working model
LLM_BASE_URL = "https://router.huggingface.co/v1" 

# Embedding Service (Google Colab)
COLAB_API_URL = "https://pseudoclerically-nonlisting-kimberley.ngrok-free.dev"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "logs/quran_search.log"