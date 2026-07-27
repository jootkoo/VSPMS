import pydantic

class RAGChunkAndSrc(pydantic.BaseModel): #result after we source and chunk the pdf
    chunks: list[str]
    source_id: str = None 

class RAGUpsertResult(pydantic.BaseModel): #result after we upsert a doc
    ingested: int

class RAGSearchResult(pydantic.BaseModel): #searching for some text 
    contexts: list[str]
    sources: list[str]

class RAGQueryResult(pydantic.BaseModel): #Query user sends to the endpoint 
    answer: str
    sources: list[str]
    num_contexts: int 