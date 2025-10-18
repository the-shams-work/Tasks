from __future__ import annotations

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int | None = Field(None, description="The unique identifier of the task")

    title: str = Field(..., description="The title of the task")
    description: str | None = Field(None, description="A detailed description of the task")
    status: str = Field("pending", description="The current status of the task")


    class Config:
        json_schema_extra = {
            "example": {
                "title": "Implement authentication",
                "description": "Create user login and registration functionality",
            }
        }
