import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routes import upload, query, metadata

load_dotenv()

app = FastAPI(
    title="DocuMind AI API",
    description="A document question-answering API powered by retrieval-augmented generation.",
    version="1.0.0",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:8501").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(metadata.router, prefix="/upload/metadata", tags=["Metadata"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the DocuMind AI API"}
