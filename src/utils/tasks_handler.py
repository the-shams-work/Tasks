from __future__ import annotations

from collections import defaultdict

import aiosqlite

from src.models import Task

with open("schema.sql") as schema_file:
    SCHEMA = schema_file.read()


class TasksHandler:
    def __init__(self):
        self.schema = SCHEMA
        self.db: aiosqlite.Connection | None = None
        self.cached_tasks: dict[int, defaultdict] = defaultdict(defaultdict)

    async def init(self):
        self.db = await aiosqlite.connect("database.sqlite")
        await self.db.executescript(self.schema)
        await self.db.commit()

    async def close(self):
        if self.db is not None:
            await self.db.close()

    async def create_task(self, *, user_id: int, task: Task):
        query = r"""
            INSERT INTO 
                tasks
                    (user_id, title, description, status)
            VALUES
                (?, ?, ?, ?)
            RETURNING
                id
        """
        values = (user_id, task.title, task.description, task.status)

        assert self.db is not None, "TasksHandler is not initialised"

        cursor = await self.db.execute(query, values)
        row = await cursor.fetchone()
        await self.db.commit()

        if row is not None:
            self.cached_tasks[user_id][row[0]] = task

    async def delete_task(self, *, task_id: int, user_id: int):
        query = r"""DELETE FROM tasks WHERE id = ? AND user_id = ? RETURNING id """
        values = (task_id, user_id)

        assert self.db is not None, "TasksHandler is not initialised"

        cursor = await self.db.execute(query, values)
        row = await cursor.fetchone()
        if row is not None:
            del self.cached_tasks[user_id][task_id]

        await self.db.commit()

    async def list_tasks(self, *, user_id: int, status: str | None = None):
        base_query = "SELECT id, title, description, status, user_id, id FROM tasks WHERE user_id = ?"
        values: tuple = (user_id,)
        if status is not None:
            base_query += " AND LOWER(status) = LOWER(?)"
            values = (user_id, status)

        assert self.db is not None, "TasksHandler is not initialised"

        cursor = await self.db.execute(base_query, values)
        async for row in cursor:
            task = Task(id=row[0], title=row[1], description=row[2], status=row[3])
            self.cached_tasks[row[4]][row[0]] = task

            yield task

    async def get_task(self, *, task_id: int, user_id: int) -> Task | None:
        try:
            return self.cached_tasks[user_id][task_id]
        except KeyError:
            pass

        query = """SELECT title, description, status, user_id FROM tasks WHERE id = ? AND user_id = ?"""
        values = (task_id, user_id)

        assert self.db is not None, "TasksHandler is not initialised"

        cursor = await self.db.execute(query, values)
        row = await cursor.fetchone()

        if row is None:
            return None

        return Task(title=row[0], description=row[1], status=row[2], id=task_id)

    async def update_task(self, *, task_id: int, user_id: int, task: Task):
        query = r"""
            UPDATE 
                tasks
            SET
                title = ?,
                description = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE
                id = ? AND user_id = ?
        """
        values = (task.title, task.description, task.status, task_id, user_id)

        assert self.db is not None, "TasksHandler is not initialised"

        await self.db.execute(query, values)
        await self.db.commit()
