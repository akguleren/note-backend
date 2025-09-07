from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache
import os


class Settings(BaseSettings):
    # Firebase Configuration
    firebase_project_id: str = ""
    firebase_private_key_id: str = ""
    firebase_private_key: str = ""
    firebase_client_email: str = ""
    firebase_client_id: str = ""
    firebase_auth_uri: str = "https://accounts.google.com/o/oauth2/auth"
    firebase_token_uri: str = "https://oauth2.googleapis.com/token"
    firebase_auth_provider_x509_cert_url: str = (
        "https://www.googleapis.com/oauth2/v1/certs"
    )
    firebase_client_x509_cert_url: str = ""

    # API Configuration
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    debug: bool = True

    # CORS Configuration
    allowed_origins: str = (
        "http://localhost:3000,http://localhost:8080,http://localhost:5173"
    )

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()
