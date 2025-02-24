import logging
from http import HTTPStatus

from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse

from oauth_login_evaluation.user.manager import (
    connect_social_account,
    get_user_by_id,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/connect_social_account")
async def post_connect_social_account(
    user_id: str = Form(...),
    provider: str = Form(...),
    account_key: str = Form(...),
):
    logger.info(
        f"""Connecting social account for user_id: {user_id}, provider: {provider}, account_key: {account_key}"""
    )

    # * Check if user exists
    user = get_user_by_id(user_id)
    if not user:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "user_not_found"})

    social_account = connect_social_account(user_id=user.id, provider=provider, account_key=account_key)

    return JSONResponse(content=social_account.dict())
