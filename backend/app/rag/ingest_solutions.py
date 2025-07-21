from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import logging

load_dotenv()

docs = []

DATA_DIR = Path("app/data/solutions")
if not DATA_DIR.exists():
    raise FileNotFoundError(f"Data directory {DATA_DIR} not found")

for csv_path in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(csv_path)
    for row in df.itertuples():
        content = (
            f"Title: {row.title}\n"
            f"Solutions: {row.solutions}\n"
        )
        docs.append(Document(page_content=content))
logging.info(f"{len(docs)} upload document")

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=80,
    chunk_overlap=20
)
chunks = text_splitter.split_documents(docs)
logging.info(f"{len(chunks)} chunks")

embeddings = OpenAIEmbeddings()

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="vector_store/solutions_vector_store"
)
print("vector created")
