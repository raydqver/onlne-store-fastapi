from typing import Annotated

from fastapi import Depends, HTTPException, status, Cookie
from jwt import InvalidTokenError
from core.utils.jwt import decode_jwt
from core import settings, logger


def get_token_payload(
    token: Annotated[str, Cookie(alias=settings.auth_jwt.cookie_key_token)],
) -> dict[str, str | int]:
    """
    Декодирует токен и возвращает полезную нагрузку из него
    :param token: токен
    :return: полезная нагрузка в токене.
    """
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError:
        logger.exception("Токен невалиден")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token error",
        )
    return payload


def get_user_id(payload: Annotated[dict, Depends(get_token_payload)]) -> int:
    """
    Получает id пользователя
    :param payload: Annotated[dict, Depends(get_token_payload)])
    :return: id пользователя
    """
    return int(payload.get("sub"))


UserIdDep = Annotated[int, Depends(get_user_id)]
