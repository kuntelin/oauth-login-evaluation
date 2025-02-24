import uuid
from typing import Optional

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(sa_column_kwargs={"unique": True})
    email: str = Field(sa_column_kwargs={"unique": True})
    is_active: bool = True
    is_superuser: bool = False


def user_id_default():
    return str(uuid.uuid4())


class User(UserBase, table=True):
    id: Optional[str] = Field(default_factory=user_id_default, primary_key=True)
    hashed_password: str
    salt: str


class SocialAccount(SQLModel, table=True):
    provider: str = Field(primary_key=True, nullable=False, index=True)
    account_key: str = Field(primary_key=True, nullable=False, index=True)
    user_id: str = Field(primary_key=True, foreign_key="user.id", index=True)


class Token(SQLModel, table=True):
    provider: str = Field(primary_key=True, nullable=False, index=True)
    token: str = Field(primary_key=True, nullable=False, index=True)
    is_active: bool = True
    expires_in: int = Field()
    user_id: str = Field(primary_key=True, foreign_key="user.id")
