from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
#allows to upload and search for vectors 

class QdrantStorage:
    def __init__(self, url="http://localhost:6333", collection="docs", dim=3072):
        self.client = QdrantClient(url=url, timeout=30) #if dont connect in 30 seconds program crashes
        self.collection = collection
        if not self.client.collection_exists(self.collection): #checks if we already have collection called "docs", if dont creates one
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE) #calculating diff points in vectors
            )
    def upsert(self, ids, vectors, payloads): #insert and update func
        #payload is the readable info we vectorized 
        #grabs all associate ids, vectors and payloads to create point structure and insert it
        points = [PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i]) for i in range(len(ids))]
        self.client.upsert(self.collection, points=points)

    def search(self, query_vector, top_k: int=5): #top_k means we're looking for 5 results from the vector database
        results = self.client.search(
            collection_name = self.collection,
            query_vector=query_vector, 
            with_payload=True, 
            limit=top_k
        )
        context = []
        sources = []

        for r in results:
            payload = getattr(r, "payload", None) or {}
            text = payload.get("text", "")
            source = payload.get("source", "")
            if texts:
                context.append(text)
                sources.append(source)
        return {"contexts": contexts, "sources":list(sources)}