# app/routes/metadata.py
from fastapi import APIRouter
from app.db.metadata import get_all_metadata

router = APIRouter()

@router.get("/")
def read_metadata():
    return get_all_metadata()
