from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.models import transform_entities
from app.models.sql.user import User, UserIn, UserOut
from app.repository.user import UserRepository
from app.utils.passw import verify_password


async def create_user(
    db_session: AsyncSession,
    payload: UserIn,
) -> UserOut:
    user = await User.create(db_session, **payload.model_dump())
    user = UserOut.model_validate(user)
    return user


async def get_user_by_username(
    db_session: AsyncSession,
    username: EmailStr,
) -> UserOut:
    users_repository = UserRepository(db_session)
    user = await users_repository.get_by_username(username)
    return UserOut.model_validate(user) if user else None


async def get_user(
    user_id: UUID,
    db_session: AsyncSession,
) -> Optional[UserOut]:
    query = select(User).where(User.id == user_id, User.enabled is True)
    user = await db_session.exec(query)
    user = user.first()
    return UserOut.model_validate(user) if user else None


async def get_all_users(db_session: AsyncSession) -> List[UserOut]:
    users_repository = UserRepository(db_session)
    users = await users_repository.list()
    return transform_entities(users, UserOut) if users else None


async def update_user(
    user_id: UUID,
    user: UserIn,
    db_session: AsyncSession,
) -> UserOut:
    users_repository = UserRepository(db_session)
    user = await users_repository.update(user_id, user)
    return UserOut.model_validate(user) if user else None


async def delete_user(user_id: UUID, db_session: AsyncSession) -> bool:
    users_repository = UserRepository(db_session)
    res = await users_repository.delete(user_id)
    return res


async def authenticate_user(
    db_session: AsyncSession,
    username: str,
    password: str,
) -> Optional[UserOut]:
    users_repository = UserRepository(db_session)
    user = await users_repository.get_by_username(username)
    if not user or not verify_password(password, user.password):
        return None
    return UserOut.model_validate(user)
