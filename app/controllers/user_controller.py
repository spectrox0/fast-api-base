from ast import List

from sqlalchemy.orm import Session

from app.models.user import UserSchema, UserSerializer
from app.services import user_services


async def create_user(
    user: UserSchema,
    db_session: Session,
) -> UserSerializer:
    return user_services.create_user(db_session, user)


async def get_user(
    user_id: str,
    db_session=Session,
) -> UserSerializer:
    user_id = int(user_id)
    user = user_services.get_user(db_session=db_session, user_id=user_id)
    return user


async def get_all_users(db_session: Session) -> List[UserSerializer]:
    users = await user_services.get_all_users(db_session)
    return users


async def update(
    user_id: str,
    user: UserSchema,
    db_session: Session,
) -> UserSerializer:
    user_id = int(user_id)
    user = await user_services.update(
        db_session,
        id=user_id,
        **user.model_dump(),
    )
    return user


async def delete_user(user_id: str, db_session: Session) -> bool:
    user_id = int(user_id)
    return await user_services.delete_user(user_id, db_session)
