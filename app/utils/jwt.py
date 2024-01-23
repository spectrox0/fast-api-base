from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.utils.exceptions import ForbiddenException
from config.settings import settings


class JWTRepo:
    def __init__(self, data: dict = None, token: str = None):
        self.data = data or {}
        self.token = token

    def generate_token(self, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = self.data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(
            to_encode,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )

        return encode_jwt

    def decode_token(self) -> dict:
        try:
            decode_token = jwt.decode(
                self.token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
            return (
                decode_token
                if decode_token["expires"] >= datetime.time()
                else None
            )
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
            return {}

    @staticmethod
    def extract_token(token: str):
        return jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request,
        )
        if (
            not credentials
            or not credentials.scheme == "Bearer"
            or not self.verify_jwt(credentials.credentials)
        ):
            raise ForbiddenException
        return credentials.credentials

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        try:
            jwt.decode(
                jwt_token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False
