from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

client = MongoClient("mongodb://localhost:27017/")
db = client["note_app"]
users_collection = db["users"]

# Schemas
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Signup route
@router.post("/signup")
def signup(user: UserCreate):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    result = users_collection.insert_one(user_dict)
    return {"id": str(result.inserted_id), "name": user.name, "email": user.email, "role": user.role}

# Login route
@router.post("/login")
def login(data: LoginRequest):
    user = users_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not pwd_context.verify(data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")

    user_out = {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"]
    }
    return user_out  
@router.get("/users/children")
def get_children():
    children = list(users_collection.find({"role": "child"}))
    for c in children:
        c["_id"] = str(c["_id"])
    return [{"id": c["_id"], "name": c["name"], "email": c["email"]}]
