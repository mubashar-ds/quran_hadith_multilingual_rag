from fastapi import FastAPI
from api.routes import router
from services.logger import logger
import uvicorn

app = FastAPI(
    title="Quran Search API",
    version="1.2.0",
    description="Islamic Quran Search with Hybrid Search (Dense + Sparse) and LLM Explanations",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(router)

@app.on_event("startup")
async def startup():
    logger.info("🚀 Quran Search API Starting...")
    logger.info("✅ Hybrid Search Enabled")
    logger.info("✅ LLM Explanations Enabled")
    logger.info("✅ PostgreSQL Integration Ready")

if __name__ == "__main__":
    logger.info("Starting server on http://0.0.0.0:8000")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )