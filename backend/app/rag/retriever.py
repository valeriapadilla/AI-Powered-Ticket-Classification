import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()
VECTOR_STORE_DIR = "vector_store"

def default_k() -> int:
    try:
        return int(os.getenv("RETRIEVER_K", 3))
    except ValueError:
        return 3

def get_retriever(k: int = None):
    """
    Load the persisted Chroma vector store and return a retriever.
    Args:
        k: number of similar chunks to retrieve (defaults to RETRIEVER_K env or 3).
    Returns:
        A LangChain retriever instance.
    """
    if k is None:
        k = default_k()

    vs = Chroma(
        persist_directory=VECTOR_STORE_DIR,
        embedding_function=OpenAIEmbeddings(),
    )

    return vs.as_retriever(search_kwargs={"k": k})

