import logging
import inngest
from inngest.experimental import ai
from dotenv import load_dotenv
import uuid
import os
from openai import OpenAI
from rag_ai.data_loader import load_and_chunk_pdf, embed_texts
from rag_ai.vector_db import QdrantStorage
from rag_ai.custom_types import (
    RAGChunkAndSrc,
    RAGSearchResult,
    RAGUpsertResult,
)


load_dotenv()

inngest_client = inngest.Inngest(
    app_id="rag_app",
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=inngest.PydanticSerializer()
)


#helper search function - used by both the direct API query and the Inngest query
def search_manual(question: str, top_k: int = 5) -> RAGSearchResult:
    if not question.strip():
        raise ValueError("Question is required.")

    query_vec = embed_texts([question])[0] #question needs to be embedded
    store = QdrantStorage()
    found = store.search(query_vec, top_k) #searched based on q vec

    return RAGSearchResult(
        contexts=found["contexts"],
        sources=found["sources"]
    )


#direct query function - allows main.py to return the answer directly to Streamlit
def query_manual(question: str, top_k: int = 5):
    found = search_manual(question, top_k)

    if not found.contexts:
        return {
            "answer": "No relevant manual content was found.",
            "sources": [],
            "num_contexts": 0
        }

    context_block = "\n\n".join(
        f"- {context}" for context in found.contexts
    ) #join all the sentences found

    #this is the prompt for the AI
    user_content = (
        "Use the following context to answer the question.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {question}\n"
        "Answer concisely using the context above."
    )

    #initialize AI
    client = OpenAI()

    #the inference
    #temperature is how random the model will be
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You answer questions using only the provided context."
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
    )

    #get the answer
    answer = response.choices[0].message.content.strip()

    return {
        "answer": answer,
        "sources": found.sources,
        "num_contexts": len(found.contexts)
    }


#ingest function - used to monitor and track progress within certain functions
#within ingest function has steps
#npx inngest-cli@latest dev -u http://127.0.0.1:8000/api/inngest --no-discovery
@inngest_client.create_function(
    fn_id="RAG: Ingest PDF",
    trigger=inngest.TriggerEvent(event="rag/ingest_pdf")
)
#this func runs when triggered
async def rag_ingest_pdf(ctx: inngest.Context):

    def _load() -> RAGChunkAndSrc: #load
        pdf_path = ctx.event.data["pdf_path"] #get path
        source_id = ctx.event.data.get("source_id", pdf_path)
        chunks = load_and_chunk_pdf(pdf_path) #chunk the pdf

        return RAGChunkAndSrc(
            chunks=chunks,
            source_id=source_id
        ) #return the result

    def _upsert(
        chunks_and_src: RAGChunkAndSrc
    ) -> RAGUpsertResult: #add to vector database

        chunks = chunks_and_src.chunks
        source_id = chunks_and_src.source_id
        vecs = embed_texts(chunks)

        ids = [
            str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    f"{source_id}:{i}"
                )
            )
            for i in range(len(chunks))
        ] #create unique identifier

        payloads = [
            {
                "source": source_id,
                "text": chunks[i]
            }
            for i in range(len(chunks))
        ] #looping through all the chunks and getting text and source id for payload

        #now we got our peramters we cna pass through to quadrant storage
        QdrantStorage().upsert(ids, vecs, payloads)

        return RAGUpsertResult(
            ingested=len(chunks)
        )

    chunks_and_src = await ctx.step.run(
        "load-and-chunk",
        _load,
        output_type=RAGChunkAndSrc
    ) #initializing the step, lambda because we want to call w/ arguments

    ingested = await ctx.step.run(
        "embed-and-upsert",
        lambda: _upsert(chunks_and_src),
        output_type=RAGUpsertResult
    ) #load from the previous step

    return ingested.model_dump()


#query funciton
@inngest_client.create_function(
    fn_id="RAG: Query",
    trigger=inngest.TriggerEvent(event="rag/query_pdf_ai")
)
async def rag_query_pdf_ai(ctx: inngest.Context):

    question = ctx.event.data["question"] #the question
    top_k = int(ctx.event.data.get("top_k", 5))

    found = await ctx.step.run(
        "embed-and-search",
        lambda: search_manual(question, top_k),
        output_type=RAGSearchResult
    )

    context_block = "\n\n".join(
        f"- {c}" for c in found.contexts
    ) #join all the sentences found

    #this is the prompt for the AI
    user_content = (
        "Use the following context to answer the question.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {question}\n"
        "Answer concisely using the context above."
    )

    #initialize AI
    adapter = ai.openai.Adapter(
        auth_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini"
    )

    #the inference
    #temperature is how random the model will be
    res = await ctx.step.ai.infer(
        "llm-answer",
        adapter=adapter,
        body={
            "max_tokens": 1024,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": "You answer questions using only the provided context."
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ]
        }
    )

    #get the answer
    answer = res["choices"][0]["message"]["content"].strip()

    return {
        "answer": answer,
        "sources": found.sources,
        "num_contexts": len(found.contexts)
    }


#initialize the api in main.py instead of this file
#uvicorn main:app --reload

#main.py imports:
#inngest_client
#query_manual
#rag_ingest_pdf
#rag_query_pdf_ai

#docker run -d --name qdrant -p 6333:6333 -v "$(pwd)/qdrant_storage:/qdrant/storage" qdrant/qdrant allows use to run qdrant locally, created container
