import httpx
from config.settings import COLAB_API_URL
from services.logger import logger
import traceback

async def get_embeddings_from_colab(query: str):
    """
    Get both dense and sparse embeddings from Colab backend
    """
    try:
        logger.info(f"📡 Calling Colab API: {COLAB_API_URL}/embed")
        logger.info(f"Query: '{query}'")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{COLAB_API_URL}/embed",
                json={"text": query},
                headers={"Content-Type": "application/json"}
            )
            
            logger.info(f"Colab response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Colab API successful")
                
                # Extract embeddings from the correct structure
                if "embeddings" in result:
                    embeddings_data = result["embeddings"]
                    logger.info(f"Embeddings keys: {list(embeddings_data.keys())}")
                    
                    # Get dense vector
                    dense_vector = embeddings_data.get("dense_vector", [])
                    if not dense_vector:
                        dense_vector = embeddings_data.get("dense", [])
                    
                    # Get sparse vectors
                    sparse_data = embeddings_data.get("sparse", {})
                    if isinstance(sparse_data, dict):
                        sparse_indices = sparse_data.get("indices", [])
                        sparse_values = sparse_data.get("values", [])
                    else:
                        sparse_indices = []
                        sparse_values = []
                    
                    embeddings = {
                        "dense": dense_vector if isinstance(dense_vector, list) else [],
                        "sparse": {
                            "indices": sparse_indices if isinstance(sparse_indices, list) else [],
                            "values": sparse_values if isinstance(sparse_values, list) else []
                        }
                    }
                    
                    processed_text = result.get("text", query)
                    
                else:
                    # Fallback: maybe embeddings are at root level
                    logger.warning("No 'embeddings' key found, checking root level")
                    dense_vector = result.get("dense_vector", result.get("dense", []))
                    
                    embeddings = {
                        "dense": dense_vector if isinstance(dense_vector, list) else [],
                        "sparse": {
                            "indices": result.get("sparse_indices", result.get("indices", [])),
                            "values": result.get("sparse_values", result.get("values", []))
                        }
                    }
                    processed_text = result.get("text", result.get("processed_text", query))
                
                # Validate embeddings
                if len(embeddings["dense"]) != 1024:
                    logger.warning(f"Dense vector length is {len(embeddings['dense'])} (expected 1024)")
                    # If not 1024, pad or truncate
                    if len(embeddings["dense"]) < 1024:
                        # Pad with zeros
                        embeddings["dense"] = embeddings["dense"] + [0.0] * (1024 - len(embeddings["dense"]))
                        logger.info(f"Padded dense vector to 1024 dimensions")
                    elif len(embeddings["dense"]) > 1024:
                        # Truncate
                        embeddings["dense"] = embeddings["dense"][:1024]
                        logger.info(f"Truncated dense vector to 1024 dimensions")
                
                logger.info(f"✅ Dense vector: {len(embeddings['dense'])} dim")
                logger.info(f"✅ Sparse indices: {len(embeddings['sparse']['indices'])}")
                logger.info(f"✅ Sparse values: {len(embeddings['sparse']['values'])}")
                logger.info(f"✅ Processed text: '{processed_text}'")
                
                return embeddings, processed_text
                
            else:
                error_msg = f"Colab API error {response.status_code}: {response.text[:200]}"
                logger.error(error_msg)
                raise Exception(error_msg)
                
                
    except Exception as e:
        logger.error(f"🚨 Embedding service error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Fallback: Return dummy embeddings
        dummy_embeddings = {
            "dense": [0.01] * 1024,
            "sparse": {"indices": [1, 2, 3, 4, 5], "values": [0.1, 0.2, 0.15, 0.1, 0.05]}
        }
        logger.info("Using fallback dummy embeddings")
        return dummy_embeddings, query