from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

router = APIRouter()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["note_app"]
notes_collection = db["notes"]

# Schemas
class NoteCreate(BaseModel):
    title: str
    content: str
    user_id: str

class NoteUpdate(BaseModel):
    title: str
    content: str

# Get notes for a user
@router.get("/notes/{user_id}")
def get_notes(user_id: str):
    notes = list(notes_collection.find({"user_id": user_id}))
    for note in notes:
        note["_id"] = str(note["_id"])
    return notes

# Create a new note
@router.post("/notes")
def create_note(note: NoteCreate):
    note_dict = note.dict()
    result = notes_collection.insert_one(note_dict)
    note_dict["_id"] = str(result.inserted_id)
    return note_dict

# Update a note
@router.put("/notes/{note_id}")
def update_note(note_id: str, note: NoteUpdate):
    result = notes_collection.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": note.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    updated_note = notes_collection.find_one({"_id": ObjectId(note_id)})
    updated_note["_id"] = str(updated_note["_id"])
    return updated_note

# Delete a note
@router.delete("/notes/{note_id}")
def delete_note(note_id: str):
    result = notes_collection.delete_one({"_id": ObjectId(note_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"detail": "Note deleted successfully"}
