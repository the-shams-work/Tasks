from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Request, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.app import tasks_handler, token_handler
from src.models import Task
from src.utils import Token

security = HTTPBearer()


def get_user_token(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = token_handler.decode_token(credentials.credentials)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return token


router = APIRouter(prefix="/tasks")


@router.post("/")
async def create_tasks(task: Task = Body(...), token: Token = Depends(get_user_token)):
    user_id = int(token.sub)
    await tasks_handler.create_task(user_id=user_id, task=task)

    return {"success": True}


@router.get("/")
async def get_tasks(status: str | None = Query(None, description="Filter by status: pending|completed"), token: Token = Depends(get_user_token)):
    user_id = int(token.sub)

    return [task async for task in tasks_handler.list_tasks(user_id=user_id, status=status)]


@router.put("/{id}")
async def update_task(id: int = Path(...), task: Task = Body(...), token: Token = Depends(get_user_token)):
    user_id = int(token.sub)
    await tasks_handler.update_task(user_id=user_id, task_id=id, task=task)

    return {"success": True}


@router.delete("/{id}")
async def delete_task(id: int = Path(...), token: Token = Depends(get_user_token)):
    user_id = int(token.sub)
    await tasks_handler.delete_task(user_id=user_id, task_id=id)

    return {"success": True}
