from typing import Annotated

from fastapi import Cookie, Depends
from jwt import InvalidTokenError
from starlette.responses import Response

from core import logger, settings
from core.utils.jwt import decode_jwt
from frontend.schemas.user import UserIsAuthenticatedSchema


def get_token_payload_without_exc(
    response: Response,
    token: Annotated[
        str | None, Cookie(alias=settings.auth_jwt.cookie_key_token)
    ] = None,
) -> dict[str, str | int] | None:
    """
    Декодирует токен и возвращает полезную нагрузку из него
    :param response: Response
    :param token: токен
    :return: полезная нагрузка в токене.
    """
    if not token:
        return None
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        logger.exception("Токен невалиден")
        response.delete_cookie(key=settings.auth_jwt.cookie_key_token)
        return None
    return payload


async def get_user(
    payload: Annotated[dict | None, Depends(get_token_payload_without_exc)],
) -> UserIsAuthenticatedSchema:
    if payload is None:
        return UserIsAuthenticatedSchema(is_authenticated=False)
    return UserIsAuthenticatedSchema(
        is_authenticated=True,
        username=payload.get("username"),
    )


UserDep = Annotated[UserIsAuthenticatedSchema, Depends(get_user)]
