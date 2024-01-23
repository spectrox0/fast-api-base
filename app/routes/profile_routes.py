from typing import List

from fastapi import Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

import app.controllers.profile_controller as controller
from app.models.profile import ProfileSchema, ProfileSerializer
from app.utils.router import get_api_router
from config.database import get_session

router = get_api_router("profiles")


@router.get(
    "/",
    response_model=List[ProfileSchema],
    status_code=status.HTTP_200_OK,
)
async def get_profiles(
    db_session: AsyncSession = Depends(get_session),
):
    return await controller.get_profiles(db_session)


@router.delete(
    "/{profile_id}",
    response_model=ProfileSerializer,
    status_code=status.HTTP_200_OK,
)
async def delete_profile(
    profile_id: str,
    db_session: AsyncSession = Depends(get_session),
):
    """
    Delete a profile with the given profile_id.

    Args:
        profile_id (str): The ID of the profile to be deleted.
        db_session (Session, optional): The database session. Defaults to Depends(db.get_db).
        status_code (int, optional): The HTTP status code to be returned. Defaults to status.HTTP_200_OK.

    Returns:
        The result of the delete operation.
    """
    return await controller.delete_profile(profile_id, db_session)


@router.put(
    "/{profile_id}",
    response_model=ProfileSerializer,
    status_code=status.HTTP_200_OK,
)
async def update_profile(
    profile_id: str,
    profile: ProfileSchema,
    db_session: AsyncSession = Depends(get_session),
):
    """
    Update a profile with the given profile_id using the provided profile data.

    Args:
        profile_id (str): The ID of the profile to be updated.
        profile (ProfileSchema): The updated profile data.
        db_session (Session, optional): The database session. Defaults to Depends(db.get_db).
        status_code (int, optional): The HTTP status code to be returned. Defaults to status.HTTP_200_OK.

    Returns:
        The updated profile.
    """
    return await controller.update_profile(profile_id, profile, db_session)


@router.post(
    "/",
    response_model=ProfileSerializer,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    profile: ProfileSchema,
    db_session: AsyncSession = Depends(get_session),
):
    """
    Create a new profile.

    Args:
        profile (ProfileSchema): The profile data to be created.
        db_session (Session, optional): The database session. Defaults to Depends(db.get_db).

    Returns:
        The created profile.
    """
    return await controller.create_profile(profile, db_session)
