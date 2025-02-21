from fastapi import APIRouter
from fastapi.responses import (
    JSONResponse,
    PlainTextResponse,
)

from oauth_login_evaluation import settings
from oauth_login_evaluation.auth.keycloak.utils import get_keycloak_auth_controller

router = APIRouter()

auth_controller = get_keycloak_auth_controller(settings)


@router.get("/sso")
async def sso():
    return PlainTextResponse(content=auth_controller.get_auth_url())


@router.get("/callback")
def callback(code: str):
    print(f"code: {code}")

    token = auth_controller.get_token(
        code=code, grant_type="authorization_code", redirect_uri=settings.KEYCLOAK_REDIRECT_URI
    )
    print(f"token: {token}")

    user_info = auth_controller.get_user_info(access_token=token["access_token"])

    return JSONResponse(content={"token": token, "user_info": user_info})
