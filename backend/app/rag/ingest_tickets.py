from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

docs = []

DATA_DIR = Path("app/data/tickets")
if not DATA_DIR.exists():
    raise FileNotFoundError(f"Data directory {DATA_DIR} not found")

for csv_path in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(csv_path)
    for row in df.itertuples():
        content = (
            f"Title: {row.title}\n"
            f"Description: {row.description}\n"
        )
        metadata = {
            "id": row.id,
            "title": row.title,
            "level": row.level, #l1,l2,l3
            "priority": row.priority, #low, medium, high
            "ETA": row.ETA,
        }
        docs.append(Document(page_content=content, metadata=metadata))
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
    persist_directory="./vector_store/it_tickets_vector_store"
)
print("vector created ")
