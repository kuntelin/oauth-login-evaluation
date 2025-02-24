from sqlmodel import Session, create_engine

from oauth_login_evaluation import settings

__all__ = [
    "get_engine",
    "get_session",
]

# engine = create_engine(settings.DATABASE_URL)


def get_engine():
    return create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})


def get_session():
    return Session(get_engine())
