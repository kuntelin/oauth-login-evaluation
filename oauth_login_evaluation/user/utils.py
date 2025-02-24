from sqlmodel import SQLModel

from oauth_login_evaluation.common.utils import (
    get_engine,
    get_session,
)

from .models import (
    SocialAccount,  # noqa: F401
    Token,  # noqa: F401
    User,  # noqa: F401
)


def init_db():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


def prepare_db():
    session = get_session()
    user = User(
        username="admin",
        email="admin@localhost.localdomain",
        hashed_password="admin",
        salt="admin",
        is_active=True,
        is_superuser=True,
    )
    session.add(user)
    session.commit()
