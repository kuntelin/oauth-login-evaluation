import logging

from fastapi import APIRouter
from fastapi.responses import (
    JSONResponse,
    PlainTextResponse,
)

from oauth_login_evaluation import settings
from oauth_login_evaluation.auth.line.utils import get_line_auth_controller

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
    user_info = auth_controller.get_user_info(token["access_token"])

    return JSONResponse(content={"token": token, "user_info": user_info})
