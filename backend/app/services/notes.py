import firebase_admin
from firebase_admin import firestore
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from ..models import NoteCreate, NoteUpdate, NoteResponse
from ..models.common import ServiceResponse
from .firebase import initialize_firebase


class NotesService:
    def __init__(self):
        # Initialize Firebase if not already done
        firebase_app = initialize_firebase()
        if firebase_app is None:
            # Development mode - use mock database
            self.db = None
            self.collection = "notes"
            self._mock_notes = {}  # Simple in-memory storage for development
            print("Running in development mode with mock database")
        else:
            self.db = firestore.client()
            self.collection = "notes"

    async def create_note(
        self, note_data: NoteCreate, user_id: str
    ) -> ServiceResponse[NoteResponse]:
        """Create a new note for the authenticated user"""
        try:
            # Generate unique ID for the note
            note_id = str(uuid.uuid4())
            now = datetime.utcnow()

            # Prepare note document
            note_doc = {
                "id": note_id,
                "user_id": user_id,
                "title": note_data.title,
                "content": note_data.content,
                "created_at": now,
                "updated_at": now,
            }

            if self.db is None:
                # Development mode - store in memory
                self._mock_notes[note_id] = note_doc
            else:
                # Save to Firestore
                doc_ref = self.db.collection(self.collection).document(note_id)
                doc_ref.set(note_doc)

            note_response = NoteResponse(**note_doc)
            return ServiceResponse(
                type=True, message="Note created successfully", data=note_response
            )

        except Exception as e:
            return ServiceResponse(
                type=False, message=f"Failed to create note: {str(e)}"
            )

    async def get_user_notes(self, user_id: str) -> ServiceResponse[List[NoteResponse]]:
        """Get all notes for the authenticated user"""
        try:
            if self.db is None:
                # Development mode - filter mock notes
                user_notes = [
                    note
                    for note in self._mock_notes.values()
                    if note["user_id"] == user_id
                ]

                # Sort by creation date (newest first)
                user_notes.sort(key=lambda x: x["created_at"], reverse=True)

                notes = [NoteResponse(**note) for note in user_notes]

                return ServiceResponse(
                    type=True,
                    message=f"Retrieved {len(notes)} notes successfully",
                    data=notes,
                )
            else:
                # Firestore mode
                query = self.db.collection(self.collection).where(
                    "user_id", "==", user_id
                )

                # Order by creation date (newest first)
                query = query.order_by(
                    "created_at", direction=firestore.Query.DESCENDING
                )

                # Execute query
                docs = query.stream()
                notes = []

                for doc in docs:
                    note_data = doc.to_dict()
                    notes.append(NoteResponse(**note_data))

                return ServiceResponse(
                    type=True,
                    message=f"Retrieved {len(notes)} notes successfully",
                    data=notes,
                )

        except Exception as e:
            return ServiceResponse(
                type=False, message=f"Failed to fetch notes: {str(e)}"
            )

    async def get_note_by_id(
        self, note_id: str, user_id: str
    ) -> ServiceResponse[Optional[NoteResponse]]:
        """Get a specific note by ID for the authenticated user"""
        try:
            if self.db is None:
                # Development mode - get from mock notes
                note_data = self._mock_notes.get(note_id)
                if not note_data or note_data["user_id"] != user_id:
                    return ServiceResponse(
                        type=False,
                        message="Note not found or you don't have permission to access it",
                    )
                note_response = NoteResponse(**note_data)
                return ServiceResponse(
                    type=True,
                    message="Note retrieved successfully",
                    data=note_response,
                )
            else:
                # Firestore mode
                doc_ref = self.db.collection(self.collection).document(note_id)
                doc = doc_ref.get()

                if not doc.exists:
                    return ServiceResponse(type=False, message="Note not found")

                note_data = doc.to_dict()

                # Verify ownership
                if note_data["user_id"] != user_id:
                    return ServiceResponse(
                        type=False,
                        message="You don't have permission to access this note",
                    )

                note_response = NoteResponse(**note_data)
                return ServiceResponse(
                    type=True,
                    message="Note retrieved successfully",
                    data=note_response,
                )

        except Exception as e:
            return ServiceResponse(
                type=False, message=f"Failed to fetch note: {str(e)}"
            )

    async def update_note(
        self, note_id: str, note_data: NoteUpdate, user_id: str
    ) -> ServiceResponse[Optional[NoteResponse]]:
        """Update a note for the authenticated user"""
        try:
            if self.db is None:
                # Development mode - update mock note
                existing_data = self._mock_notes.get(note_id)
                if not existing_data or existing_data["user_id"] != user_id:
                    return ServiceResponse(
                        type=False,
                        message="Note not found or you don't have permission to update it",
                    )

                # Update the note
                if note_data.title is not None:
                    existing_data["title"] = note_data.title
                if note_data.content is not None:
                    existing_data["content"] = note_data.content

                existing_data["updated_at"] = datetime.utcnow()

                note_response = NoteResponse(**existing_data)
                return ServiceResponse(
                    type=True,
                    message="Note updated successfully",
                    data=note_response,
                )
            else:
                # Firestore mode
                doc_ref = self.db.collection(self.collection).document(note_id)
                doc = doc_ref.get()

                if not doc.exists:
                    return ServiceResponse(type=False, message="Note not found")

                existing_data = doc.to_dict()

                # Verify ownership
                if existing_data["user_id"] != user_id:
                    return ServiceResponse(
                        type=False,
                        message="You don't have permission to update this note",
                    )

                # Prepare update data
                update_data = {}
                if note_data.title is not None:
                    update_data["title"] = note_data.title
                if note_data.content is not None:
                    update_data["content"] = note_data.content

                # Always update the timestamp
                update_data["updated_at"] = datetime.utcnow()

                # Update the document
                doc_ref.update(update_data)

                # Return updated document
                updated_doc = doc_ref.get()
                note_response = NoteResponse(**updated_doc.to_dict())
                return ServiceResponse(
                    type=True,
                    message="Note updated successfully",
                    data=note_response,
                )

        except Exception as e:
            return ServiceResponse(
                type=False, message=f"Failed to update note: {str(e)}"
            )

    async def delete_note(self, note_id: str, user_id: str) -> ServiceResponse[bool]:
        """Delete a note for the authenticated user"""
        try:
            if self.db is None:
                # Development mode - delete from mock notes
                note_data = self._mock_notes.get(note_id)
                if not note_data or note_data["user_id"] != user_id:
                    return ServiceResponse(
                        type=False,
                        message="Note not found or you don't have permission to delete it",
                    )

                del self._mock_notes[note_id]
                return ServiceResponse(
                    type=True, message="Note deleted successfully", data=True
                )
            else:
                # Firestore mode
                doc_ref = self.db.collection(self.collection).document(note_id)
                doc = doc_ref.get()

                if not doc.exists:
                    return ServiceResponse(type=False, message="Note not found")

                note_data = doc.to_dict()

                # Verify ownership
                if note_data["user_id"] != user_id:
                    return ServiceResponse(
                        type=False,
                        message="You don't have permission to delete this note",
                    )

                # Delete the document
                doc_ref.delete()
                return ServiceResponse(
                    type=True, message="Note deleted successfully", data=True
                )

        except Exception as e:
            return ServiceResponse(
                type=False, message=f"Failed to delete note: {str(e)}"
            )

        except Exception as e:
            return ServiceResponse(
                type="error", message=f"Failed to delete note: {str(e)}"
            )


# Create service instance
notes_service = NotesService()
