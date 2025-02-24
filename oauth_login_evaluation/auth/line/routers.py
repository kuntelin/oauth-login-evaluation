import logging
from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import (
    JSONResponse,
    PlainTextResponse,
)

from oauth_login_evaluation import settings
from oauth_login_evaluation.auth.line.utils import get_line_auth_controller
from oauth_login_evaluation.user.manager import add_token, get_user_by_social_account

logger = logging.getLogger(__name__)

router = APIRouter()

auth_controller = get_line_auth_controller(settings)


@router.get("/sso")
def sso():
    return PlainTextResponse(content=auth_controller.get_auth_url())


@router.get("/callback")
def callback(code: str):
    logger.info(f"code: {code}")

    token = auth_controller.get_token(code)

    # * get social user info
    social_user = auth_controller.get_user_info(token["access_token"])
    logger.debug(f"social_user: {social_user}")

    # * get local user by social account
    local_user = get_user_by_social_account(provider="line", account_key=social_user["userId"])
    logger.debug(f"local_user: {local_user}")

    # * local user not found
    # FIXME: should redirect to signup page if local user not found
    if not local_user:
        return JSONResponse(status_code=HTTPStatus.OK, content={"token": token, "social_user": social_user})

    # * local user found, add token to db
    add_token(user_id=local_user.id, token=token["access_token"], provider="line", expires_in=token["expires_in"])

    # * return social token, social user info, local user info
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"token": token, "social_user": social_user, "local_user": local_user.dict()},
    )
