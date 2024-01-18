from typing import List

from sqlalchemy.orm import Session

from app.models.user import UserSchema, UserSerializer


async def create_user(
    db_session: Session,
    user: UserSchema,
) -> UserSerializer:
    user = await UserSchema.create(db_session, **user.model_dump())
    return user


async def get_user(
    user_id: int,
    db_session: Session,
) -> UserSerializer:
    user = await UserSchema.get(db_session, id=user_id)
    return user


async def get_all_users(db_session: Session) -> List[UserSerializer]:
    users = await UserSchema.get_all(db_session)
    return users


async def update(
    user_id: int,
    user: UserSchema,
    db_session: Session,
) -> UserSerializer:
    user = await UserSchema.update(db_session, id=user_id, **user.model_dump())
    return user


async def delete_user(user_id: int, db_session: Session) -> bool:
    return await UserSchema.delete(db_session, id=user_id)
