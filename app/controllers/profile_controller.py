""" Profile controller. """
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

import app.services.profile_services as services
from app.models.profile import ProfileSchema, ProfileSerializer
from app.utils.msg import not_entities_found, not_entity_found


async def get_profiles(db_session: Session) -> List[ProfileSerializer]:
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
            raise HTTPException(
                status_code=404,
                detail=not_entities_found("profiles"),
            )
        return res
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        ) from exc


async def delete_profile(
    profile_id: str,
    db_session: Session,
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
            raise HTTPException(status_code=404, detail="Profile not found")
        return res
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        ) from exc


def update_profile(
    profile_id: str,
    profile: ProfileSchema,
    db_session: Session,
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
        res = services.update_profile(
            id=int(profile_id),
            profile=profile,
            db_session=db_session,
        )
        if not res:
            raise HTTPException(
                status_code=404,
                detail=not_entity_found("Profile"),
            )
        return res
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        ) from exc


async def get_profile(
    profile_id: str,
    db_session: Session,
) -> ProfileSerializer:
    try:
        res = await services.get_profile(
            int(profile_id),
            db_session,
        )
        if not res:
            raise HTTPException(
                status_code=404,
                detail=not_entity_found("Profile"),
            )
        return res
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        ) from exc


async def create_profile(
    profile: ProfileSchema,
    db_session: Session,
) -> ProfileSerializer:
    try:
        res = await services.create_profile(
            profile,
            db_session,
        )
        if not res:
            raise HTTPException(
                status_code=400,
                detail="The profile could not be created",
            )
        return res
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        ) from exc
