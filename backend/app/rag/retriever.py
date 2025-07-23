import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from pathlib import Path

load_dotenv()

def default_k() -> int:
    try:
        return int(os.getenv("RETRIEVER_K", 3))
    except ValueError:
        return 3

def get_retriever(vector_store_path="vector_store", k: int = None):
    if k is None:
        k = default_k()

    base_dir = Path(__file__).resolve().parent 
    abs_vector_store_path = str(base_dir / vector_store_path)
    vs = Chroma(
        persist_directory=abs_vector_store_path,
        embedding_function=OpenAIEmbeddings(),
    )
 
    return vs.as_retriever(search_kwargs={"k": k})