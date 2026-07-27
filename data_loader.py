#use llama index to load pdf documents and to embed them 
from openai import OpenAI
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv

load_dotenv()

client = OpenAI() #pulls from openai key

#chunk / break down pdf into smaller pieces and then embed those small pieces 
