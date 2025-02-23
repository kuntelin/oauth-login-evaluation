import logging
from datetime import (
    datetime,
    timedelta,
    timezone,
)

import jwt
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.responses import (
    JSONResponse,
    PlainTextResponse,
)
from fastapi.security import OAuth2PasswordRequestForm

from oauth_login_evaluation import settings
from oauth_login_evaluation.auth.line.utils import get_line_auth_controller

logger = logging.getLogger(__name__)

router = APIRouter()

auth_controller = get_line_auth_controller(settings)


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update(
        {
            "iss": "oauth_login_evaluation",
            "sub": to_encode.get("username"),
            "exp": to_encode.get("expires_in", datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION)),
            "typ": to_encode.get("token_type", "bearer"),
        }
    )
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "admin" and form_data.password == "admin":
        expires_in = (datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION)).second
        return JSONResponse(
            content={
                "token_type": "bearer",
                "expires_in": expires_in,
                "access_token": create_access_token({"username": form_data.username}),
            },
            status_code=200,
        )
    else:
        return PlainTextResponse(content="Invalid username or password")
