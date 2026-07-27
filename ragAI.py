import logging
from fastapi import FastAPI
import inngest
import inngest.fast_api
from inngest.experimental import ai
from dotenv import load_dotenv
import uuid
import os
import datetime
from data_loader import load_and_chunk_pdf, embed_texts 
from vector_db import QdrantStorage
from custom_types import RAGChunkAndSrc, RAGQueryResult, RAGSearchResult, RAGUpsertResult



load_dotenv()

inngest_client = inngest.Inngest(
    app_id="rag_app",
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=inngest.PydanticSerializer()
)

#ingest function 
#npx inngest-cli@latest dev -u http://127.0.0.1:8000/api/inngest --no-discovery
@inngest_client.create_function(
    fn_id="RAG: Ingest PDF",
    trigger=inngest.TriggerEvent(event="rag/ingest_pdf")
)
#this func runs when triggered
async def rag_ingest_pdf(ctx: inngest.Context):
    return{"hello": "world"}

#uvicorn ragAI:app
app = FastAPI()

inngest.fast_api.serve(app, inngest_client, [rag_ingest_pdf])


#docker run -d --name qdrant -p 6333:6333 -v "$(pwd)/qdrant_storage:/qdrant/storage" qdrant/qdrant allows use to run qdrant locally, created container