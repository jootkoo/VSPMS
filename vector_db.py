from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
#allows to upload and search for vectors 

class QdrantStorage:
    def __init__(self, url="http://localhost:6333", collection="docs", dim=3072):
        self.client = QdrantClient(url=url, timeout=60) #if dont connect in 30 seconds program crashes
        self.collection = collection
        if not self.client.collection_exists(self.collection): #checks if we already have collection called "docs", if dont creates one
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE) #calculating diff points in vectors
            )
    
    #Updated upsert, send to DB in batches for larger PDFS (instruction manuals)
    def upsert(self, ids, vecs, payloads, batch_size: int = 100):
        points = [
            {"id": ids[i], "vector": vecs[i], "payload": payloads[i]}
            for i in range(len(ids))
        ]
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(self.collection, points=batch)

    def search(self, query_vector, top_k: int=5): #top_k means we're looking for 5 results from the vector database
        response = self.client.query_points(
            collection_name = self.collection,
            query=query_vector, 
            with_payload=True, 
            limit=top_k
        )
        contexts = []
        sources = []
        for result in response.points:
            payload = getattr(result, "payload", None) or {}
            text = payload.get("text", "")
            source = payload.get("source", "")
            if text:
                contexts.append(text)
                sources.append(source)
        return {"contexts": contexts, "sources":list(sources)}