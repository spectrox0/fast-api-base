from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_403_FORBIDDEN

from app.main import app

security = HTTPBearer()


@app.middleware("http")
async def validate_token(request: Request, call_next):
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )
    authorization: str = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise credentials_exception
    if not is_token_valid(param):
        raise credentials_exception

    response = await call_next(request)
    return response


def is_token_valid(token: str):
    return True
