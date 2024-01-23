from fastapi import Depends, Request

from app.main import app
from app.services.user_services import get_user
from app.utils.jwt import JWTBearer
from config.database import get_session

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.middleware("http")
async def auth_middleware(
    request: Request,
    call_next,
    db_session=Depends(get_session),
):
    res = JWTBearer(request)
    print(res)
    # response = await validate_token(request)

    request.state.current_user = await get_user(
        user_id="sas",
        db_session=db_session,
    )
    response = await call_next(request)
    return response
