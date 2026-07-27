#use llama index to load pdf documents and to embed them 
from openai import OpenAI
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv

load_dotenv()

client = OpenAI() #pulls from openai key

EMBED_MODEL = "text-embedding-3-large"
EMBED_DIM = 3072 #make sure matches in vectordb
#chunk / break down pdf into smaller pieces and then embed those small pieces 
splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200) #overlapp of 200 characters incase for context

def load_and_chunk_pdf(path: str):
    docs = PDFReader().load_data(file=path) #look for pdf then load
    texts = [d.text for d in docs if getattr(d, "text", None)] #get all the text in every doc inside the document if the doc has text ( not images )
    chunks = []
    for t in texts:
        chunks.extend(splitter.split_text(t))
    return chunks

def embed_texts(texts: list[str]) ->list[list[float]]: #sends a request to openAI, -> means thats what the return type is expected to be 
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=texts,  #passes all of the texts thats been chunked up and embed them (turn into vector)
    )
    return [item.embedding for item in response.data] #go through the response and pull out the embedded data



