import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

def default_k() -> int:
    try:
        return int(os.getenv("RETRIEVER_K", 3))
    except ValueError:
        return 3

def get_retriever(vector_store_path="vector_store", k: int = None):
    if k is None:
        k = default_k()

    vs = Chroma(
        persist_directory=vector_store_path,
        embedding_function=OpenAIEmbeddings(),
    )

    return vs.as_retriever(search_kwargs={"k": k})

