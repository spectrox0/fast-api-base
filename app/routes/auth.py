from fastapi import Depends, Request, status

from app.controllers.user_controller import authenticate_user
from app.models.sql.user import UserIn, UserOut
from app.models.user import UserSerializer
from app.utils.router import get_api_router
from config.database import get_session

router = get_api_router("auth")


@router.post(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserOut,
)
def get_user_me(request: Request):
    return request.state.user


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=UserSerializer,
)
async def login_user(
    user: UserIn,
    db_session=Depends(get_session),
):
    return await authenticate_user(db_session, user.username, user.password)
