from sqlmodel import Session, create_engine

from oauth_login_evaluation.core import settings

__all__ = [
    "get_engine",
    "get_session",
]


def get_engine():
    return create_engine(settings.DATABASE_URL, echo=settings.TRACING)


def get_session():
    return Session(get_engine())
