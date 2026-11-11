import os
import re
from typing import List

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_DIR = "vector_store"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
_embeddings = None


def _get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embeddings


def retrieve_chunks(document_id: str, query: str, k: int = 5) -> List[str]:
    # IDs are generated as UUIDs by the upload endpoint; reject path traversal.
    if not re.fullmatch(r"[0-9a-fA-F-]{36}", document_id):
        raise ValueError("Invalid document ID.")

    index_path = os.path.join(VECTOR_DIR, document_id)
    if not os.path.isdir(index_path):
        raise FileNotFoundError("Document index was not found.")

    # Only load indexes created by this application in its own local storage.
    vectorstore = FAISS.load_local(
        index_path,
        _get_embeddings(),
        allow_dangerous_deserialization=True,
    )
    results = vectorstore.similarity_search(query, k=max(1, min(k, 10)))
    return [result.page_content for result in results]
