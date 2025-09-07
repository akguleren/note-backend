#!/usr/bin/env python3
"""
Startup script for the Notes API
"""
import uvicorn
import os
from app.main import app
from app.core.config import get_settings

if __name__ == "__main__":
    settings = get_settings()

    # Use environment variables or defaults
    host = os.getenv("API_HOST", settings.api_host)
    port = int(os.getenv("API_PORT", settings.api_port))
    reload = os.getenv("DEBUG", str(settings.debug)).lower() == "true"

    uvicorn.run("app.main:app", host=host, port=port, reload=reload, log_level="info")
