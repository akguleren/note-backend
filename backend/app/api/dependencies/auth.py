from fastapi import Depends, HTTPException, status
from ...services.auth import verify_token
from ...models.common import ServiceResponse


async def get_current_user(
    user_response: ServiceResponse[dict] = Depends(verify_token),
) -> dict:
    """
    Get current authenticated user
    """
    if user_response.type == False:  # Error case
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=user_response.message,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_response.data
