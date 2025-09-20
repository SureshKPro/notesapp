from pydantic import BaseModel, EmailStr
from typing import Optional, List

# User
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  
    parent_id: Optional[str] = None

class UserOut(BaseModel):
    id: str
    name: str
    email: str
    role: str

# Notes
class NoteBase(BaseModel):
    title: str
    content: str
    folder: Optional[str] = None
    tags: Optional[List[str]] = []
    is_checked: Optional[bool] = False

class NoteCreate(NoteBase):
    pass

class NoteOut(NoteBase):
    id: str
    user_id: str
