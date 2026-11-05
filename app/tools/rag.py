from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from app.config import settings
import uuid
from typing import List

encoder = SentenceTransformer("BAAI/bge-small-zh-v1.5")
client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

def ensure_collection():
    collections = client.get_collections().collections
    if not any(c.name == settings.COLLECTION_NAME for c in collections):
        client.create_collection(
            collection_name=settings.COLLECTION_NAME,
            vectors_config=VectorParams(size=512, distance=Distance.COSINE),
        )

def search_rag(query: str, top_k: int = 3) -> List[str]:
    try:
        ensure_collection()
        query_vector = encoder.encode(query).tolist()
        results = client.query_points(
            collection_name=settings.COLLECTION_NAME, query=query_vector, limit=top_k
        )
        return [hit.payload.get("text", "") for hit in results.points]
    except Exception as e:
        print(f"[RAG Tool Error]: {e}")
        return []

def add_documents(texts: List[str], metadatas: List[dict] = None):
    ensure_collection()
    if metadatas is None: metadatas = [{} for _ in texts]
    points = []
    for text, meta in zip(texts, metadatas):
        vector = encoder.encode(text).tolist()
        points.append(PointStruct(id=str(uuid.uuid4()), vector=vector, payload={"text": text, **meta}))
    client.upsert(collection_name=settings.COLLECTION_NAME, points=points)