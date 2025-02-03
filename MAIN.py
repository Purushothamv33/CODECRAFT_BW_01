from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from uuid import uuid4
from typing import Dict

app = FastAPI()

# In-memory storage (HashMap equivalent)
users_db: Dict[str, dict] = {}

# User model for input validation
class User(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserResponse(User):
    id: str

@app.post("/users/", response_model=UserResponse, status_code=201)
def create_user(user: User):
    user_id = str(uuid4())
    users_db[user_id] = user.dict()
    return {"id": user_id, **user.dict()}

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **users_db[user_id]}

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, updated_user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = updated_user.dict()
    return {"id": user_id, **updated_user.dict()}

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return
