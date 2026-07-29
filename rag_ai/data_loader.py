# use llama index to load pdf documents and to embed them
from openai import OpenAI
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv
import tiktoken

load_dotenv()

client = OpenAI()  # pulls from openai key

EMBED_MODEL = "text-embedding-3-large"
EMBED_DIM = 3072  # make sure matches in vectordb
MAX_TOKENS_PER_REQUEST = 250000  # stay under OpenAI's 300k/request cap
MAX_ITEMS_PER_REQUEST = 2048       # OpenAI also caps items per request

# chunk / break down pdf into smaller pieces and then embed those small pieces
splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200)  # overlap of 200 characters in case for context

_encoding = tiktoken.get_encoding("cl100k_base")  # works for embedding-3 models


def load_and_chunk_pdf(path: str):
    docs = PDFReader().load_data(file=path)  # look for pdf then load
    texts = [d.text for d in docs if getattr(d, "text", None)]  # get all the text in every doc inside the document if the doc has text (not images)
    chunks = []
    for t in texts:
        chunks.extend(splitter.split_text(t))
    return chunks

#here is create batches by tokens
def _batch_by_tokens(texts: list[str], max_tokens: int = MAX_TOKENS_PER_REQUEST, max_items: int = MAX_ITEMS_PER_REQUEST) -> list[list[str]]:
    batches = []
    current_batch = []
    current_tokens = 0

    for text in texts:
        n_tokens = len(_encoding.encode(text))
        if current_batch and (current_tokens + n_tokens > max_tokens or len(current_batch) >= max_items): #if not at limit add to the batch
            batches.append(current_batch)
            current_batch = []
            current_tokens = 0
        current_batch.append(text)
        current_tokens += n_tokens

    if current_batch:
        batches.append(current_batch)

    return batches

#the send off 
def embed_texts(texts: list[str]) -> list[list[float]]:  # sends a request to openAI, -> means thats what the return type is expected to be
    all_embeddings = []
    for batch in _batch_by_tokens(texts):
        response = client.embeddings.create(
            model=EMBED_MODEL,
            input=batch,  # passes one safe-sized batch of chunks to embed
        )
        all_embeddings.extend(item.embedding for item in response.data)
    return all_embeddings