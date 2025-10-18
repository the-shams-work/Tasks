from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.utils import TasksHandler, TokenHandler, UserHandler

token_handler = TokenHandler("some_secret_key")
tasks_handler = TasksHandler()
user_handler = UserHandler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await tasks_handler.init()
    await user_handler.init()
    try:
        yield
    finally:
        await tasks_handler.close()
        await user_handler.close()


app = FastAPI(title="Task Management API", version="1.0.0", lifespan=lifespan)

from src.routes import api_router, web_router

app.include_router(api_router)
app.include_router(web_router, include_in_schema=False)
