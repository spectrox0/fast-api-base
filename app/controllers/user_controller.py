""" User controller module. """
from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.sql.user import UserIn, UserOut
from app.services import user_services
from app.utils.exceptions import EmailAlreadyUsedException


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
    user_id: str,
    db_session: AsyncSession,
) -> UserOut:
    user = await user_services.get_user(db_session=db_session, user_id=user_id)
    return user


async def get_all_users(db_session: AsyncSession) -> List[UserOut]:
    users = await user_services.get_all_users(db_session)
    return users


async def update(
    user_id: str,
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

    user = await user_services.update(
        db_session,
        id=user_id,
        **user.model_dump(),
    )
    return user


async def delete_user(user_id: str, db_session: AsyncSession) -> bool:
    user_id = int(user_id)
    return await user_services.delete_user(user_id, db_session)
