from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
from typing import Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions and return standardized error responses"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": False,
            "message": exc.detail,
            "data": None,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    errors = []
    for error in exc.errors():
        errors.append(
            {
                "field": " -> ".join([str(loc) for loc in error["loc"]]),
                "message": error["msg"],
                "type": error["type"],
            }
        )

    return JSONResponse(
        status_code=422,
        content={
            "type": False,
            "message": "Validation Error: The request contains invalid data",
            "data": {"validation_errors": errors},
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unexpected error occurred: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "type": False,
            "message": "Internal Server Error: An unexpected error occurred. Please try again later.",
            "data": None,
        },
    )
