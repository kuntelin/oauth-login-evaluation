import logging
from http import HTTPStatus

from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.responses import (
    JSONResponse,
)
from fastapi.security import OAuth2PasswordRequestForm

from oauth_login_evaluation.auth.local.utils import create_access_token
from oauth_login_evaluation.user.manager import (
    add_token,
    authenticate_user,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"Login: {form_data.username}")

    # * authenticate user
    user = authenticate_user(form_data.username, form_data.password)

    # * user not exist or password is incorrect
    if user is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "Invalid username or password"})

    # * create access token
    access_token, expires_in = create_access_token({"username": user.username})

    # * add token to database
    add_token(provider="local", token=access_token, expires_in=expires_in, user_id=user.id)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={
            "token_type": "bearer",
            "expires_in": expires_in,
            "access_token": access_token,
            "user": user.dict(),
        },
    )
