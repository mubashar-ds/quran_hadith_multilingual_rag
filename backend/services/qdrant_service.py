from qdrant_client import QdrantClient
from qdrant_client.models import SparseVector
from config.settings import QDRANT_URL, QDRANT_DENSE_COLLECTION, QDRANT_SPARSE_COLLECTION
from services.logger import logger
import traceback

class HybridQdrantService:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, timeout=30)
        self.dense_collection = QDRANT_DENSE_COLLECTION
        self.sparse_collection = QDRANT_SPARSE_COLLECTION
        
        logger.info(f"✅ Hybrid Qdrant initialized")
        logger.info(f"  Dense: {self.dense_collection}")
        logger.info(f"  Sparse: {self.sparse_collection}")
        
        # Verify collections
        self._verify_collections()
    
    def _verify_collections(self):
        """Verify both collections exist"""
        try:
            for col_name in [self.dense_collection, self.sparse_collection]:
                info = self.client.get_collection(col_name)
                logger.info(f"✓ {col_name}: {info.points_count} points")
        except Exception as e:
            logger.error(f"Collection verification error: {e}")
    
    def hybrid_search(self, embeddings, top_k=5):
        """
        Perform hybrid search using both dense and sparse vectors
        """
        try:
            dense_vector = embeddings["dense"]
            sparse_indices = embeddings["sparse"]["indices"]
            sparse_values = embeddings["sparse"]["values"]
            
            logger.info(f"🔍 Hybrid search: dense={len(dense_vector)} dim, sparse={len(sparse_indices)} indices")
            
            # 1. Search dense collection
            logger.info("Searching dense collection...")
            dense_results = self._search_dense(dense_vector, top_k * 2)
            
            # 2. Search sparse collection (if sparse data exists)
            sparse_results = []
            if sparse_indices and len(sparse_indices) > 0:
                logger.info("Searching sparse collection...")
                sparse_results = self._search_sparse(sparse_indices, sparse_values, top_k * 2)
            
            # 3. Combine results
            combined_results = self._combine_results(dense_results, sparse_results, top_k)
            
            logger.info(f"✅ Found {len(combined_results)} combined results")
            return combined_results
            
        except Exception as e:
            logger.error(f"Hybrid search error: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Fallback to dense-only
            try:
                logger.info("Trying dense-only fallback...")
                return self._search_dense(embeddings["dense"], top_k)
            except Exception as e2:
                logger.error(f"Dense fallback also failed: {e2}")
                raise
    
    def _search_dense(self, dense_vector, limit):
        """Search dense collection"""
        try:
            # Use query_points for Qdrant v1.9.0
            search_result = self.client.query_points(
                collection_name=self.dense_collection,
                query=dense_vector,
                limit=limit,
                with_payload=True
            )
            logger.info(f"Dense search returned {len(search_result.points)} points")
            return search_result.points
        except Exception as e:
            logger.error(f"Dense search error: {e}")
            raise
    
    def _search_sparse(self, indices, values, limit):
        """Search sparse collection"""
        try:
            sparse_vector = SparseVector(indices=indices, values=values)
            
            # Try with named vector approach
            search_result = self.client.query_points(
                collection_name=self.sparse_collection,
                query={"name": "sparse", "vector": sparse_vector},
                limit=limit,
                with_payload=True
            )
            logger.info(f"Sparse search returned {len(search_result.points)} points")
            return search_result.points
            
        except Exception as e:
            logger.warning(f"Sparse search failed: {e}")
            return []
    
    def _combine_results(self, dense_results, sparse_results, top_k):
        """
        Simple combination: prefer dense results, add sparse if unique
        """
        from collections import OrderedDict
        
        # Start with dense results
        combined = OrderedDict()
        for point in dense_results:
            combined[point.id] = point
        
        # Add unique sparse results
        if sparse_results:
            for point in sparse_results:
                if point.id not in combined:
                    combined[point.id] = point
        
        # Convert to list and take top_k
        results_list = list(combined.values())[:top_k]
        
        # Ensure each result has score attribute
        for i, point in enumerate(results_list):
            if not hasattr(point, 'score'):
                point.score = 1.0 - (i * 0.01)  # Assign dummy score
        
        return results_list
    
    def search(self, embeddings, top_k=5):
        """Main search method"""
        return self.hybrid_search(embeddings, top_k)

# Initialize service
qdrant_service = HybridQdrantService()