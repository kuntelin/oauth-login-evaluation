import uuid
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

__all__ = [
    "User",
    "UserOut",
    "SocialAccount",
    "Token",
]


def user_id_default():
    return str(uuid.uuid4())


class _UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False


class User(_UserBase, table=True):
    id: Optional[str] = Field(default_factory=user_id_default, primary_key=True)
    hashed_password: str


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool
    is_superuser: bool

    class Config:
        extra = "ignore"


class SocialAccount(SQLModel, table=True):
    user_id: str = Field(primary_key=True, foreign_key="user.id", index=True)
    provider: str = Field(primary_key=True, nullable=False, index=True)
    account_key: str = Field(nullable=False, index=True)


class Token(SQLModel, table=True):
    provider: str = Field(primary_key=True, nullable=False, index=True)
    token: str = Field(primary_key=True, nullable=False, index=True)
    revoked: bool = Field(default=False)
    expires_in: int = Field()
    user_id: str = Field(primary_key=True, foreign_key="user.id", description="For quick access to user object")
