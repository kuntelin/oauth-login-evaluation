from passlib.context import CryptContext
from sqlmodel import SQLModel

from oauth_login_evaluation.core.database import (
    get_engine,
    get_session,
)

from .models import (
    SocialAccount,  # noqa: F401
    Token,  # noqa: F401
    User,  # noqa: F401
)

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_db():
    engine = get_engine()
    SQLModel.metadata.create_all(bind=engine)


def prepare_db():
    session = get_session()
    user = User(
        username="admin",
        email="admin@localhost.localdomain",
        hashed_password=hash_password("admin"),
        is_active=True,
        is_superuser=True,
    )
    session.add(user)
    session.commit()


def hash_password(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return passwd_context.verify(plain_password, hashed_password)
