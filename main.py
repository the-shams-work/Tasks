from __future__ import annotations

import asyncio
import os

import uvicorn

from src import app

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass

if __name__ == "__main__":
    uvicorn.run(app)
