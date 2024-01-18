""" Profile services. """ ""
from typing import List

from sqlalchemy.orm import Session

from app.models.profile import ProfileSchema, ProfileSerializer


async def get_profiles(db_session: Session) -> List[ProfileSerializer]:
    return await ProfileSchema.get_all(db_session)


async def get_profile(id: int, db_session: Session) -> ProfileSerializer:
    return await ProfileSchema.get(db_session, id=id)


async def delete_profile(id: int, db_session: Session) -> ProfileSerializer:
    return await ProfileSchema.delete(db_session, id=id)


async def update_profile(
    id: int,
    profile: ProfileSchema,
    db_session: Session,
) -> ProfileSerializer:
    return await ProfileSchema.update(
        db_session,
        id=id,
        **profile.model_dump(),
    )


async def create_profile(
    profile: ProfileSchema,
    db_session: Session,
) -> ProfileSerializer:
    return await ProfileSchema.create(db_session, **profile.model_dump())
