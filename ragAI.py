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

#ingest function - used to monitor and track progress within certain functions
#within ingest function has steps 
#npx inngest-cli@latest dev -u http://127.0.0.1:8000/api/inngest --no-discovery
@inngest_client.create_function(
    fn_id="RAG: Ingest PDF",
    trigger=inngest.TriggerEvent(event="rag/ingest_pdf")
)
#this func runs when triggered

async def rag_ingest_pdf(ctx: inngest.Context):
    def _load(ctx: inngest.Context) -> RAGChunkAndSrc: #load
        pdf_path = ctx.event.data["pdf_path"] #get path
        source_id = ctx.event.data.get("source_id", pdf_path)
        chunks = load_and_chunk_pdf(pdf_path) #chunk the pdf
        return RAGChunkAndSrc(chunks=chunks, source_id = source_id) #return the result

    def _upsert(chunks_and_src: RAGChunkAndSrc) -> RAGUpsertResult: #add to vector database
        chunks = chunks_and_src.chunks
        source_id = chunks_and_src.source_id
        vecs = embed_texts(chunks)
        ids = [str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source_id}:{i}")) for i in range(len(chunks))] #create unique identifier
        payloads = [{"source": source_id, "text": chunks[i]} for i in range(len(chunks))] #looping through all the chunks and getting text and source id for payload
        #now we got our peramters we cna pass through to quadrant storage
        QdrantStorage().upsert(ids, vecs, payloads)
        return RAGUpsertResult(ingested=len(chunks))

    chunks_and_src = await ctx.step.run("load-and-chunk", lambda: _load(ctx), output_type=RAGChunkAndSrc) #initializing the step, lambda because we want to call w/ arguments 
    ingested = await ctx.step.run("embed-and-upsert", lambda: _upsert(chunks_and_src), output_type=RAGUpsertResult) #load from the previous step
    return ingested.model_dump()

#uvicorn ragAI:app
app = FastAPI()

inngest.fast_api.serve(app, inngest_client, [rag_ingest_pdf])


#docker run -d --name qdrant -p 6333:6333 -v "$(pwd)/qdrant_storage:/qdrant/storage" qdrant/qdrant allows use to run qdrant locally, created container