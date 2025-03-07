import logging
from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import (
    JSONResponse,
    PlainTextResponse,
)

from oauth_login_evaluation.auth.keycloak.utils import get_keycloak_auth_controller
from oauth_login_evaluation.core import settings
from oauth_login_evaluation.user.manager import add_token, get_user_by_social_account
from oauth_login_evaluation.user.models import UserOut

logger = logging.getLogger(__name__)

router = APIRouter()

auth_controller = get_keycloak_auth_controller(settings)


@router.get("/sso")
async def sso():
    return PlainTextResponse(content=auth_controller.get_auth_url())


@router.get("/callback")
def callback(code: str):
    logger.info(f"callback triggered with code: {code}")

    # * get token
    token = auth_controller.get_token(
        code=code, grant_type="authorization_code", redirect_uri=settings.KEYCLOAK_REDIRECT_URI
    )
    logger.debug(f"token: {token}")

    # * get social user info
    social_user = auth_controller.get_user_info(access_token=token["access_token"])

    # * get local user by social account
    local_user = get_user_by_social_account(provider="keycloak", account_key=social_user["email"])
    logger.debug(f"local_user: {local_user}")

    # * local user not found, show error
    # FIXME: should redirect to signup page if local user not found
    if not local_user:
        # return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "local_user_not_found"})
        return JSONResponse(status_code=HTTPStatus.OK, content={"token": token, "social_user": social_user})

    # * local user found, add token to db
    add_token(user_id=local_user.id, token=token["access_token"], provider="keycloak", expires_in=token["expires_in"])

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"token": token, "social_user": social_user, "local_user": UserOut(**local_user.dict()).dict()},
    )
