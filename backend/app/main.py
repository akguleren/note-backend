from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import os
from dotenv import load_dotenv

from .core.config import get_settings
from .api.v1.api import api_router
from .core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)

# Load environment variables
load_dotenv()

# Create FastAPI instance
app = FastAPI(
    title="Notes API",
    description="A secure note-taking API with Firebase authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Get settings
settings = get_settings()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Notes API is running!", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "notes-api"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
