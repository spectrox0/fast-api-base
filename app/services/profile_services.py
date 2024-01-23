""" Profile services. """ ""
from typing import List

from sqlmodel import insert, select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.models import transform_entities
from app.models.sql.profile import Profile, ProfileIn, ProfileOut


async def get_profiles(db_session: AsyncSession) -> List[ProfileOut]:
    query = select(Profile).where(ProfileOut.enabled is True)
    profiles = await db_session.exec(query)
    profiles = profiles.all()
    if not profiles:
        return None
    # Transform the profiles into a list of ProfileOut models.
    profiles = transform_entities(profiles, ProfileOut)
    return profiles


async def get_profile(
    profile_id: str,
    db_session: AsyncSession,
) -> ProfileOut:
    query = select(Profile).where(
        Profile.id == profile_id,
        Profile.enabled is True,
    )
    profile = await db_session.exec(query)
    profile = profile.first()
    if not profile:
        return None
    profile = ProfileOut.model_validate(profile)
    return profile


async def delete_profile(
    profile_id: str,
    db_session: AsyncSession,
) -> bool:
    query = (
        update(Profile)
        .where(Profile.id == profile_id)
        .values(enabled=False)
        .returning(Profile)
    )
    profile = await db_session.exec(query)
    profile = profile.first()
    return profile is not None


async def update_profile(
    profile_id: str,
    profile: ProfileIn,
    db_session: AsyncSession,
) -> ProfileOut:
    query = (
        update(Profile)
        .where(Profile.id == profile_id)
        .values(**profile.model_dump())
        .returning(Profile)
    )
    profile = await db_session.exec(query)
    profile = profile.first()
    if not profile:
        return None
    profile = ProfileOut.model_validate(profile)
    return profile


async def create_profile(
    profile: ProfileIn,
    db_session: AsyncSession,
) -> ProfileOut:
    query = insert(Profile).values(**profile.model_dump()).returning(Profile)
    profile = await db_session.exec(query)
    db_session.commit()
    return ProfileOut.model_validate(profile) if profile else None
