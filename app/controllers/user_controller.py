""" User controller module. """
from typing import List
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.sql.user import UserIn, UserOut
from app.services import user_services
from app.utils.exceptions import (
    AuthorizationException,
    EmailAlreadyUsedException,
)


async def create_user(
    user: UserIn,
    db_session: AsyncSession,
) -> UserOut:
    # normalize username(email) and remove whitespace
    user.username = user.username.lower().strip()
    exist = await user_services.get_user_by_username(
        db_session,
        user.username,
    )
    if exist:
        raise EmailAlreadyUsedException
    return user_services.create_user(db_session, user)


async def get_user(
    user_id: UUID,
    db_session: AsyncSession,
) -> UserOut:
    user = await user_services.get_user(db_session=db_session, user_id=user_id)
    return user


async def get_all_users(db_session: AsyncSession) -> List[UserOut]:
    users = await user_services.get_all_users(db_session)
    return users


async def update(
    user_id: UUID,
    user: UserIn,
    db_session: AsyncSession,
) -> UserOut:
    # normalize username(email) and remove whitespace
    user.username = user.username.lower().strip()

    exist = await user_services.get_user_by_username(
        db_session,
        user.username,
    )
    if exist:
        raise EmailAlreadyUsedException

    user = await user_services.update_user(
        db_session,
        id=user_id,
        **user.model_dump(),
    )
    return user


async def delete_user(user_id: UUID, db_session: AsyncSession) -> bool:
    return await user_services.delete_user(user_id, db_session)


async def authenticate_user(
    db_session: AsyncSession,
    username: str,
    password: str,
) -> UserOut:
    username = username.lower().strip()
    user = await user_services.authenticate_user(
        db_session,
        username,
        password,
    )
    if not user:
        raise AuthorizationException
    return user
