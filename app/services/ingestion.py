import os
import tempfile
import shutil
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from app.utils.pdf_parser import extract_text_from_pdf

FAISS_DIR = "vector_store"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


async def process_and_store_document(file, document_id: str) -> List[str]:
    os.makedirs(FAISS_DIR, exist_ok=True)
    temp_dir = tempfile.mkdtemp(prefix="documind-")
    try:
        file_path = os.path.join(temp_dir, "uploaded.pdf")
        content = await file.read()
        if not content.startswith(b"%PDF-"):
            raise ValueError("The uploaded file is not a valid PDF.")

        with open(file_path, "wb") as output:
            output.write(content)

        text = extract_text_from_pdf(file_path)
        if not text.strip():
            raise ValueError("No extractable text was found in this PDF.")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        chunks = splitter.split_text(text)
        if not chunks:
            raise ValueError("No text chunks could be created from this PDF.")

        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
        vectorstore.save_local(os.path.join(FAISS_DIR, document_id))
        return chunks
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
