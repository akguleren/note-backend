from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Note title")
    content: str = Field(..., description="Note content")


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Note title"
    )
    content: Optional[str] = Field(None, description="Note content")


class NoteResponse(NoteBase):
    id: str = Field(..., description="Note ID")
    user_id: str = Field(..., description="User ID who owns the note")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
