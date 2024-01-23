from typing import List, Optional

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.models import transform_entities
from app.models.sql.user import User, UserIn, UserOut, select, update


async def create_user(
    db_session: AsyncSession,
    payload: UserIn,
) -> UserOut:
    user = await User.create(db_session, **payload.model_dump())
    user = UserOut.model_validate(user)
    return user


async def get_user_by_username(
    db_session: AsyncSession,
    username: str,
) -> UserOut:
    query = select(User).where(User.username == username)
    user = await db_session.exec(query)
    user = user.first()
    return UserOut.model_validate(user) if user else None


async def get_user(
    user_id: int,
    db_session: AsyncSession,
) -> Optional[UserOut]:
    query = select(User).where(User.id == user_id, User.enabled is True)
    user = await db_session.exec(query)
    user = user.first()
    return UserOut.model_validate(user) if user else None


async def get_all_users(db_session: AsyncSession) -> List[UserOut]:
    query = select(User).where(User.enabled is True)
    users = await db_session.exec(query)
    users = users.all()
    return transform_entities(users, UserOut) if users else None


async def update_user(
    user_id: str,
    user: UserIn,
    db_session: AsyncSession,
) -> UserOut:
    query = (
        update(User)
        .where(User.id == user_id)
        .values(**user.model_dump())
        .returning(User)
    )
    user = await db_session.exec(query)
    user = user.first()

    return UserOut.model_validate(user) if user else None


async def delete_user(user_id: str, db_session: AsyncSession) -> bool:
    query = (
        update(User)
        .where(User.id == user_id)
        .values(enabled=False)
        .returning(User)
    )
    user = await db_session.exec(query)
    user = user.first()
    return user is not None
