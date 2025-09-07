from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from ...models.common import ServiceResponse
from ...models import (
    NoteCreate,
    NoteUpdate,
    NoteResponse,
    MessageResponse,
)
from ...api.dependencies.auth import get_current_user
from ...services.notes import notes_service

router = APIRouter()


@router.get(
    "/notes",
    response_model=ServiceResponse[list[NoteResponse]],
    summary="List user's notes",
    description="Retrieve all notes belonging to the authenticated user",
)
async def get_notes(current_user: dict = Depends(get_current_user)):
    """
    Get all notes for the authenticated user.
    """

    result = await notes_service.get_user_notes(user_id=current_user["uid"])

    if result.type == False:  # Error case
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.message,
        )

    return result


@router.post(
    "/notes",
    response_model=ServiceResponse[NoteResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    description="Create a new note for the authenticated user",
)
async def create_note(
    note_data: NoteCreate, current_user: dict = Depends(get_current_user)
):
    """
    Create a new note.

    - **title**: Note title (required, 1-200 characters)
    - **content**: Note content (required)
    """
    result = await notes_service.create_note(
        note_data=note_data, user_id=current_user["uid"]
    )

    if result.type == False:  # Error case
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.message,
        )

    return result


@router.get(
    "/notes/{note_id}",
    response_model=ServiceResponse[NoteResponse],
    summary="Get a specific note",
    description="Retrieve a specific note by ID for the authenticated user",
)
async def get_note(note_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get a specific note by ID.

    - **note_id**: The ID of the note to retrieve
    """
    result = await notes_service.get_note_by_id(
        note_id=note_id, user_id=current_user["uid"]
    )

    if result.type == False:  # Error case
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.message,
        )

    return result


@router.put(
    "/notes/{note_id}",
    response_model=ServiceResponse[NoteResponse],
    summary="Update a note",
    description="Update an existing note for the authenticated user",
)
async def update_note(
    note_id: str, note_data: NoteUpdate, current_user: dict = Depends(get_current_user)
):
    """
    Update an existing note.

    - **note_id**: The ID of the note to update
    - **title**: Updated note title (optional, 1-200 characters)
    - **content**: Updated note content (optional)
    """
    # Validate that at least one field is being updated
    if not any(
        [
            note_data.title is not None,
            note_data.content is not None,
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update",
        )

    result = await notes_service.update_note(
        note_id=note_id, note_data=note_data, user_id=current_user["uid"]
    )

    if result.type == False:  # Error case
        if (
            "not found" in result.message.lower()
            or "permission" in result.message.lower()
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result.message,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.message,
            )

    return result


@router.delete(
    "/notes/{note_id}",
    response_model=MessageResponse,
    summary="Delete a note",
    description="Delete an existing note for the authenticated user",
)
async def delete_note(note_id: str, current_user: dict = Depends(get_current_user)):
    """
    Delete an existing note.

    - **note_id**: The ID of the note to delete
    """
    result = await notes_service.delete_note(
        note_id=note_id, user_id=current_user["uid"]
    )

    if result.type == False:  # Error case
        if (
            "not found" in result.message.lower()
            or "permission" in result.message.lower()
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result.message,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.message,
            )

    return MessageResponse(
        message=result.message,
        detail=f"Note with ID {note_id} has been permanently deleted",
    )
