from fastapi import APIRouter
from .notes import router as notes_router

api_router = APIRouter()

api_router.include_router(notes_router, tags=["notes"])
