# routes/user_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.user import User
from services.user_service import UserService

router = APIRouter()
user_service = UserService()

# Pydantic models for input validation
class UserRegisterRequest(BaseModel):
    id: int
    name: str
    email: str
    password: str
    address: str
    is_admin: bool = False

class UserLoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register", summary="Register a new user")
def register_user(request: UserRegisterRequest):
    try:
        user = User.from_dict(request.dict())
        created_user = user_service.register(user)
        return {"message": "User registered successfully", "user": created_user.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", summary="User login")
def login_user(request: UserLoginRequest):
    try:
        user = user_service.login(request.email, request.password)
        return {"message": f"Welcome back, {user.name}!", "user": user.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
