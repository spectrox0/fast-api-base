""" Profile controller. """
from typing import List
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

import app.services.profile_services as services
from app.models.profile import ProfileSchema, ProfileSerializer
from app.utils.exceptions import (
    ConflictException,
    NotFoundException,
    ServerErrorException,
)


async def get_profiles(db_session: AsyncSession) -> List[ProfileSerializer]:
    """
    Retrieve profiles from the database.

    Args:
        db_session (Session): The database session.

    Returns:
        List[ProfileSchema]: A list of profile objects.

    Raises:
        HTTPException: If no profiles are found or if there is an internal server error.
    """
    try:
        res = await services.get_profiles(db_session)
        if not res:
            raise NotFoundException(
                resource="Profiles",
            )
        return res
    except Exception as exc:
        raise ServerErrorException from exc


async def delete_profile(
    profile_id: UUID,
    db_session: AsyncSession,
) -> ProfileSchema:
    """
    Delete a profile from the database.

    Args:
        id (int): The profile id.

    Returns:
        ProfileSchema: The deleted profile.

    Raises:
        HTTPException: If the profile is not found or if there is an internal server error.
    """
    try:
        res = await services.delete_profile(int(profile_id), db_session)
        if not res:
            raise NotFoundException(resource="Profiles")
        return res
    except Exception as exc:
        raise ServerErrorException from exc


async def update_profile(
    profile_id: UUID,
    profile: ProfileSchema,
    db_session: AsyncSession,
) -> ProfileSerializer:
    """
    Update a profile in the database.

    Args:
        id (int): The profile id.

    Returns:
        ProfileSchema: The updated profile.

    Raises:
        HTTPException: If the profile is not found or if there is an internal server error.
    """
    try:
        res = await services.update_profile(
            profile_id=profile_id,
            profile=profile,
            db_session=db_session,
        )
        if not res:
            raise NotFoundException(resource="Profiles")
        return res
    except Exception as exc:
        raise ServerErrorException from exc


async def get_profile(
    profile_id: UUID,
    db_session: AsyncSession,
) -> ProfileSerializer:
    try:
        res = await services.get_profile(
            profile_id,
            db_session,
        )
        if not res:
            raise NotFoundException(resource="Profiles")
        return res
    except Exception as exc:
        raise ServerErrorException from exc


async def create_profile(
    profile: ProfileSchema,
    db_session: AsyncSession,
) -> ProfileSerializer:
    try:
        res = await services.create_profile(
            profile,
            db_session,
        )
        if not res:
            raise ConflictException
        return res
    except Exception as exc:
        raise ServerErrorException from exc
