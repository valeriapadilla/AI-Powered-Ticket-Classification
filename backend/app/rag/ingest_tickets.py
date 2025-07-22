from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

docs = []

BASE_DIR = Path(__file__).resolve().parent.parent.parent
VECTOR_STORE_DIR = BASE_DIR / "app" /"rag" /"vector_store" / "it_tickets_vector_store"

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "app" / "data" / "tickets"

for csv_path in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(csv_path)
    for row in df.itertuples():
        content = (
            f"Title: {row.title}\n"
            f"Description: {row.description}\n"
            f"Level: {row.level}\n"
            f"Priority: {row.priority}\n"
            f"ETA: {row.ETA}\n"
        )
        docs.append(Document(page_content=content))
print(f"{len(docs)} upload document")

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100,
    chunk_overlap=40
)
chunks = text_splitter.split_documents(docs)
print(f"{len(chunks)} chunks")

embeddings = OpenAIEmbeddings()

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(VECTOR_STORE_DIR)
)
print("vector created ")
