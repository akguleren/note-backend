import firebase_admin
from firebase_admin import credentials
from functools import lru_cache
from ..core.config import get_settings


@lru_cache()
def initialize_firebase():
    """Initialize Firebase Admin SDK with service account credentials"""
    try:
        print("Initializing Firebase...")
        # Check if already initialized
        if firebase_admin._apps:
            return firebase_admin.get_app()

        settings = get_settings()

        # Skip Firebase initialization if no project ID is configured
        if (
            not settings.firebase_project_id
            or settings.firebase_project_id == "test-project"
        ):
            print(
                "⚠️  Firebase not configured - authentication will be disabled for development"
            )
            return None

        # Create credentials from environment variables
        cred_dict = {
            "type": "service_account",
            "project_id": settings.firebase_project_id,
            "private_key_id": settings.firebase_private_key_id,
            "private_key": settings.firebase_private_key.replace("\\n", "\n"),
            "client_email": settings.firebase_client_email,
            "client_id": settings.firebase_client_id,
            "auth_uri": settings.firebase_auth_uri,
            "token_uri": settings.firebase_token_uri,
            "auth_provider_x509_cert_url": settings.firebase_auth_provider_x509_cert_url,
            "client_x509_cert_url": settings.firebase_client_x509_cert_url,
        }

        cred = credentials.Certificate(cred_dict)
        return firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Failed to initialize Firebase: {str(e)}")
        print("Running in development mode without Firebase authentication")
        return None
