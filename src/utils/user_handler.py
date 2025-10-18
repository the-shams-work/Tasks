from __future__ import annotations

import aiosqlite

from src.models import User

with open("schema.sql") as schema_file:
    SCHEMA = schema_file.read()


class UserHandler:
    def __init__(self):
        self.schema = SCHEMA
        self.db: aiosqlite.Connection | None = None

    async def init(self):
        self.db = await aiosqlite.connect("database.sqlite")
        await self.db.executescript(self.schema)
        await self.db.commit()

    async def close(self):
        if self.db is not None:
            await self.db.close()

    async def create_user(self, *, email: str, password: str) -> bool:
        query = r"""
            INSERT INTO 
                users
                    (email, password)
            VALUES
                (?, ?)
            RETURNING
                id, email, password
        """
        values = (email, password)

        assert self.db is not None, "UsersHandler is not initialised"

        cursor = await self.db.execute(query, values)
        row = await cursor.fetchone()
        await self.db.commit()

        return row is not None

    async def get_user(self, *, email: str, password: str) -> User | None:
        query = r"""
            SELECT 
                id, email, password
            FROM 
                users
            WHERE 
                email = ? AND password = ?
        """
        values = (email, password)

        assert self.db is not None, "UsersHandler is not initialised"

        cursor = await self.db.execute(query, values)
        row = await cursor.fetchone()

        if row is not None:
            id, user_email, user_password = row
            return User(id=id, email=user_email, password=user_password)

        return None

    async def exists(self, *, email: str) -> bool:
        query = r"""
            SELECT 
                1
            FROM 
                users
            WHERE 
                email = ?
        """
        values = (email,)

        assert self.db is not None, "UsersHandler is not initialised"

        cursor = await self.db.execute(query, values)
        row = await cursor.fetchone()

        return row is not None
