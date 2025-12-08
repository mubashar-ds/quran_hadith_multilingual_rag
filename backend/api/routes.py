from fastapi import APIRouter, HTTPException
from api.models import Query, SearchResponse
from services.embedding_service import get_embeddings_from_colab
from services.qdrant_service import qdrant_service
from services.postgres_service import get_verse_texts_from_db
from services.llm_service import get_llm_explanation
from services.logger import logger
import traceback

router = APIRouter()

@router.post("/search", response_model=SearchResponse)
async def search_quran(query: Query):
    logger.info(f"🔍 HYBRID SEARCH REQUEST")
    logger.info(f"  Query: '{query.text}'")
    logger.info(f"  Top K: {query.top_k}")
    
    try:
        # 1. Get embeddings from Colab
        logger.info("🚀 Step 1/5: Getting embeddings from Colab...")
        embeddings, processed_text = await get_embeddings_from_colab(query.text)
        
        # 2. Hybrid search in Qdrant
        logger.info("🚀 Step 2/5: Hybrid search in Qdrant...")
        try:
            hits = qdrant_service.search(embeddings, query.top_k)
            logger.info(f"✅ Qdrant search successful, got {len(hits) if hits else 0} hits")
        except Exception as qdrant_error:
            logger.error(f"❌ Qdrant search failed: {qdrant_error}")
            raise HTTPException(500, f"Qdrant search failed: {str(qdrant_error)}")
        
        if not hits:
            raise HTTPException(404, "No verses found matching your query")
        
        # 3. Extract verse details
        logger.info("🚀 Step 3/5: Extracting verse details...")
        verse_details = []
        for i, hit in enumerate(hits):
            try:
                payload = hit.payload or {}
                verse_details.append({
                    "quran_id": payload.get("quran_id"),
                    "surah_id": payload.get("surah_id"),
                    "ayah_id": payload.get("ayah_id"),
                    "juz_id": payload.get("juz_id"),
                    "surah_type": payload.get("surah_type"),
                    "hit_id": hit.id,
                    "score": float(hit.score) if hasattr(hit, 'score') else 0.0
                })
                logger.info(f"  Verse {i+1}: ID={hit.id}, Quran_ID={payload.get('quran_id')}")
            except Exception as e:
                logger.error(f"Error processing hit {i}: {e}")
                continue
        
        # 4. Get verse texts from PostgreSQL
        logger.info("🚀 Step 4/5: Fetching from PostgreSQL...")
        try:
            verse_texts = get_verse_texts_from_db(verse_details)
            logger.info(f"✅ Retrieved {len(verse_texts)} verses from PostgreSQL")
        except Exception as pg_error:
            logger.error(f"❌ PostgreSQL error: {pg_error}")
            verse_texts = []
        
        # 5. Format results
        logger.info("🚀 Step 5/5: Formatting results...")
        formatted_results = []
        for i, detail in enumerate(verse_details):
            try:
                # Match verse_text with detail by quran_id
                matched_text = next(
                    (text for text in verse_texts if text["quran_id"] == detail["quran_id"]),
                    {}
                )
                
                result = {
                    "id": detail["hit_id"],
                    "score": detail["score"],
                    "quran_id": detail["quran_id"],
                    "surah_id": detail["surah_id"],
                    "ayah_id": detail["ayah_id"],
                    "juz_id": detail["juz_id"],
                    "surah_type": detail["surah_type"],
                    "arabic_text": matched_text.get("text_ar", f"Verse {detail['quran_id']}"),
                    "english_text": matched_text.get("text_en", f"Verse {detail['quran_id']}"),
                    "urdu_text": matched_text.get("text_ur", f"آیت {detail['quran_id']}"),
                    "surah_name_ar": matched_text.get("surah_name_ar", ""),
                    "surah_name_ur": matched_text.get("surah_name_ur", ""),
                    "surah_name_en": matched_text.get("surah_name_en", ""),
                    "transliteration": matched_text.get("transliteration", "")
                }
                formatted_results.append(result)
                
                logger.info(f"  Formatted result {i+1}: Surah {detail['surah_id']}:{detail['ayah_id']}")
                
            except Exception as e:
                logger.error(f"Error formatting result {i}: {e}")
                continue
        
        # 6. Get LLM explanation
        logger.info("🤖 Getting LLM explanation...")
        try:
            arabic_texts = [result["arabic_text"] for result in formatted_results if result["arabic_text"]]
            urdu_texts = [result["urdu_text"] for result in formatted_results if result["urdu_text"]]
            verse_ids = [detail["quran_id"] for detail in verse_details]
            
            llm_explanation = get_llm_explanation(
                query.text, 
                arabic_texts, 
                urdu_texts, 
                verse_ids
            )
            logger.info(f"✅ LLM explanation generated ({len(llm_explanation.urdu)} chars)")
        except Exception as llm_error:
            logger.error(f"❌ LLM error: {llm_error}")
            llm_explanation = {
                "urdu": f"سوال '{query.text}' کے بارے میں وضاحت تیار کی جا رہی ہے۔",
                "verses_used": [detail["quran_id"] for detail in verse_details[:3]]
            }
        
        logger.info(f"🎉 SEARCH COMPLETE! Found {len(formatted_results)} verses")
        
        return SearchResponse(
            query=query.text,
            processed_query=processed_text,
            top_results=formatted_results,
            llm_explanation=llm_explanation
        )
        
    except HTTPException as http_err:
        logger.error(f"HTTP Exception: {http_err.detail}")
        raise
    except Exception as e:
        logger.error(f"🚨 UNEXPECTED ERROR in search endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(500, f"Search error: {str(e)}")

@router.get("/health")
async def health():
    logger.info("Health check request")
    return {
        "status": "healthy", 
        "service": "Quran Search API",
        "qdrant": "connected" if qdrant_service else "disconnected"
    }

@router.get("/test-qdrant")
async def test_qdrant():
    """Test Qdrant connection"""
    try:
        # Test with dummy vector
        dummy_embeddings = {
            "dense": [0.01] * 1024,
            "sparse": {"indices": [1, 2, 3], "values": [0.1, 0.2, 0.3]}
        }
        results = qdrant_service.search(dummy_embeddings, 2)
        return {
            "status": "success",
            "qdrant_working": True,
            "results_found": len(results) if results else 0,
            "message": f"Qdrant is working, found {len(results) if results else 0} results"
        }
    except Exception as e:
        return {
            "status": "error",
            "qdrant_working": False,
            "error": str(e)
        }

@router.get("/")
async def root():
    return {
        "message": "🕌 Quran Search API - Hybrid Search with LLM", 
        "status": "running",
        "version": "2.0.0",
        "endpoints": {
            "search": "POST /search",
            "health": "GET /health",
            "test_qdrant": "GET /test-qdrant",
            "docs": "GET /docs"
        }
    }