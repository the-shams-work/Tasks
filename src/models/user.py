from __future__ import annotations

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(..., description="The unique identifier of the user")
    email: str = Field(..., description="The email address of the user")
    password: str = Field(..., description="The password of the user")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "johndoe@example.com",
                "password": "securepassword123",
            }
        }
