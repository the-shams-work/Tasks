from __future__ import annotations

from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

from src.app import token_handler, user_handler

router = APIRouter(prefix="/auth")


class Credentials(BaseModel):
    email: str = Field(..., description="User's email address", examples=["user@example.com"])
    password: str = Field(..., description="User's password", examples=["securePassword123"])


@router.post("/register")
async def register_user(credentials: Credentials = Body(...)):
    user_exists = await user_handler.get_user(email=credentials.email, password=credentials.password)
    if user_exists is not None:
        return {"success": False, "message": "User already exists"}

    success = await user_handler.create_user(email=credentials.email, password=credentials.password)
    if success:
        return {"success": True, "message": "User registered successfully"}
    else:
        return {"success": False, "message": "Registration failed"}


@router.post("/login")
async def login_user(credentials: Credentials = Body(...)):
    user = await user_handler.get_user(email=credentials.email, password=credentials.password)
    if user is not None:
        token = token_handler.create_access_token(user)
        return {"success": True, "token": token}
    return {"success": False, "message": "Invalid email or password"}
