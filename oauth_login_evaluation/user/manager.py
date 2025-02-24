import logging
import uuid

from sqlmodel import select

from oauth_login_evaluation.common.utils import get_session
from oauth_login_evaluation.user.models import (
    SocialAccount,
    Token,
    User,
)

logger = logging.getLogger(__name__)


def get_user_by_id(user_id: str):
    try:
        session = get_session()
        user = session.exec(select(User).where(User.id == user_id)).one()
    except Exception as e:
        logger.error(f"Error getting user by id: {user_id}. Error: {e}")
        return None
    return user


def get_user_by_name(name: str):
    try:
        session = get_session()
        user = session.exec(select(User).where(User.username == name)).one()
    except Exception as e:
        logger.error(f"Error getting user by name: {name}. Error: {e}")
        return None
    return user


def get_user_by_social_account(provider: str, account_key: str):
    logger.info(f"Getting user by social account: {provider}, {account_key}")

    try:
        session = get_session()

        # * select social account by provider and account_key
        sql_command = (
            select(SocialAccount)
            .where(SocialAccount.provider == provider)
            .where(SocialAccount.account_key == account_key)
        )
        logger.debug(f"sql_command: {sql_command}")
        social_account = session.exec(sql_command).one()
        logger.debug(f"social_account: {social_account}")

        # * select user by social account
        sql_command = select(User).where(User.is_active == 1).where(User.id == social_account.user_id)
        logger.debug(f"sql_command: {sql_command}")
        user = session.exec(sql_command).one()
    except Exception as e:
        logger.error(f"Error getting user by social account: {e}")
        return None
    return user


def connect_social_account(user_id: uuid.UUID, provider: str, account_key: str):
    try:
        session = get_session()
        social_account = SocialAccount(user_id=user_id, provider=provider, account_key=account_key)
        session.add(social_account)
        session.commit()
    except Exception as e:
        logger.error(f"Error connecting social account: {e}")
        return False
    return social_account


def add_token(user_id: int, token: str, provider: str, expires_in: int):
    session = get_session()
    token = Token(user_id=user_id, token=token, provider=provider, expires_in=expires_in)
    session.add(token)
    session.commit()
