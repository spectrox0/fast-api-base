from fastapi import Depends, status

from app.models.user import UserSerializer
from app.utils.router import get_api_router
from config.database import get_session

router = get_api_router("auth")


@router.post(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserSerializer,
)
def get_user_me(
    db_session=Depends(get_session),
):
    pass


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=UserSerializer,
)
async def login_user(
    db_session=Depends(get_session),
):
    pass
