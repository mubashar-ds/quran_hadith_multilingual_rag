import json
from qdrant_client import QdrantClient
from qdrant_client.http import models
from tqdm import tqdm

# configuration...
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "quran_ayahs"
EMBEDDING_FILE = "Quran_Embeddings_Qdrant.jsonl"   

def get_vector_dim():
    with open(EMBEDDING_FILE, "r", encoding="utf-8") as f:
        first = json.loads(f.readline())
        dense_vec = first["vector"]["dense"]
        return len(dense_vec)

def build_sparse_vector(sparse_obj):
    if not sparse_obj:
        return None
    
    return models.SparseVector(
        indices=[int(i) for i in sparse_obj["indices"]],
        values=[float(v) for v in sparse_obj["values"]],
    )

def create_collection(client, vector_dim):
    print(f"Creating/recreating collection: {COLLECTION_NAME}")

    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            "dense": models.VectorParams(
                size=vector_dim,
                distance=models.Distance.COSINE
            )
        },
        sparse_vectors_config={
            "sparse": models.SparseVectorParams()
        }
    )
    print("Collection ready!")

def ingest_to_qdrant():
    client = QdrantClient(url=QDRANT_URL, timeout=60)

    print("Reading dimension...")
    vector_dim = get_vector_dim()

    create_collection(client, vector_dim)

    print("Starting ingestion...")

    batch = []
    batch_size = 300

    with open(EMBEDDING_FILE, "r", encoding="utf-8") as f:
        for line in tqdm(f, desc="Uploading"):
            if not line.strip():
                continue

            obj = json.loads(line)

            dense = obj["vector"]["dense"]
            sparse = build_sparse_vector(obj["vector"].get("sparse"))

            full_vector = {
                "dense": dense,
                "sparse": sparse,
            }

            point = models.PointStruct(
                id=obj["id"],
                vector=full_vector,
                payload=obj["payload"]
            )

            batch.append(point)

            if len(batch) >= batch_size:
                client.upsert(
                    collection_name=COLLECTION_NAME,
                    points=batch,
                    wait=True
                )
                batch = []

    if batch:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch,
            wait=True
        )

    print("Quran embeddings ingested into the Qdrant!")


if __name__ == "__main__":
    ingest_to_qdrant()
