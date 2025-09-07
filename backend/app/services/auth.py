from firebase_admin import auth
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .firebase import initialize_firebase
from ..models.common import ServiceResponse

# Security scheme - disable auto_error to handle 401 ourselves
security = HTTPBearer(auto_error=False)


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> ServiceResponse[dict]:
    """
    Verify Firebase ID token and return user information
    """
    try:
        # Check if credentials are provided
        if credentials is None:
            return ServiceResponse(
                type=False, message="Authorization header is missing"
            )

        # Initialize Firebase if not already done
        print("Verifying token:", credentials.credentials)

        firebase_app = initialize_firebase()

        # Check for development bypass token
        if credentials.credentials == "dev-token-123":
            user_data = {
                "uid": "dev-user-123",
                "email": "dev@example.com",
                "email_verified": True,
                "name": "Development User",
                "picture": None,
                "firebase": {"dev_mode": True, "bypass": True},
            }
            return ServiceResponse(
                type=True,
                message="Token verified successfully (development bypass)",
                data=user_data,
            )

        # Development mode - skip authentication for any token
        if firebase_app is None:
            user_data = {
                "uid": "dev-user-123",
                "email": "dev@example.com",
                "email_verified": True,
                "name": "Development User",
                "picture": None,
                "firebase": {"dev_mode": True},
            }
            return ServiceResponse(
                type=True,
                message="Token verified successfully (development mode)",
                data=user_data,
            )

        # Verify the ID token
        decoded_token = auth.verify_id_token(credentials.credentials)

        # Extract user information
        user_info = {
            "uid": decoded_token["uid"],
            "email": decoded_token.get("email"),
            "email_verified": decoded_token.get("email_verified", False),
            "name": decoded_token.get("name"),
            "picture": decoded_token.get("picture"),
            "firebase": decoded_token,
        }

        return ServiceResponse(
            type=True, message="Token verified successfully", data=user_info
        )

    except auth.InvalidIdTokenError:
        return ServiceResponse(type=False, message="Invalid authentication token")
    except auth.ExpiredIdTokenError:
        return ServiceResponse(type=False, message="Authentication token has expired")
    except Exception as e:
        print(f"Token verification failed: {str(e)}")
        return ServiceResponse(type=False, message="Could not validate credentials")
