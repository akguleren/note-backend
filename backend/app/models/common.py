from pydantic import BaseModel
from typing import Optional, Any, Generic, TypeVar

T = TypeVar("T")


class ServiceResponse(BaseModel, Generic[T]):
    """Standardized service response format

    For success responses: type=True, message describes action, data contains result
    For error responses: type=False, message describes error, data should be omitted
    """

    type: bool  # True for success, False for error
    message: str
    data: Optional[T] = None


class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None
