from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Final, TypedDict, cast

from jwt import decode, encode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from src.models import User


class Token(BaseModel):
    sub: str
    email: str
    iat: int = Field(default_factory=lambda: int(datetime.now(timezone.utc).timestamp()))
    exp: int


class TokenDict(TypedDict):
    sub: str
    email: str
    iat: int
    exp: int


class TokenHandler:
    def __init__(self, secret: str, algorithm: str = "HS256"):
        self.secret: Final[str] = secret
        self.algorithm: Final[str] = algorithm

    def create_access_token(self, user: User, expire_in: int = 60 * 60 * 24) -> str:
        payload = Token(
            sub=str(user.id),
            email=user.email,
            exp=int((datetime.now(timezone.utc) + timedelta(seconds=expire_in)).timestamp()),
        )
        token = encode(dict(payload), self.secret, algorithm=self.algorithm)
        return token

    def validate_token(self, token: str) -> Token | None:
        try:
            decoded = cast(TokenDict, decode(token, self.secret, algorithms=[self.algorithm]))
            return Token(**decoded)

        except ExpiredSignatureError:
            return None
        except InvalidTokenError:
            return None

    def decode_token(self, token: str) -> Token | None:
        return self.validate_token(token)
