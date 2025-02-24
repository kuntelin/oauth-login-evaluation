from datetime import (
    datetime,
    timedelta,
    timezone,
)

import jwt

from oauth_login_evaluation.core import settings


def create_access_token(data: dict) -> tuple[str, datetime]:
    expires_in = int((datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION)).timestamp())

    to_encode = data.copy()
    to_encode.update(
        {
            "iss": "oauth_login_evaluation",
            "sub": to_encode.get("username"),
            "exp": expires_in,
            "typ": to_encode.get("token_type", "bearer"),
        }
    )
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt, expires_in
