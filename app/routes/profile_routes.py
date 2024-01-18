from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import app.controllers.profile_controller as controller
from app.models.profile import ProfileSchema, ProfileSerializer
from config.database import db

module = "profile"
router = APIRouter(prefix="/${module}")


@router.get("/", response_model=List[ProfileSchema])
async def get_profiles(
    db_session: Session = Depends(db.get_db),
    status_code=status.HTTP_200_OK,
):
    return await controller.get_profiles(db_session)


@router.delete("/{profile_id}", response_model=ProfileSerializer)
async def delete_profile(
    profile_id: str,
    db_session: Session = Depends(db.get_db),
    status_code=status.HTTP_200_OK,
):
    return await controller.delete_profile(profile_id, db_session)


@router.put("/{profile_id}", response_model=ProfileSerializer)
async def update_profile(
    profile_id: str,
    profile: ProfileSchema,
    db_session: Session = Depends(db.get_db),
    status_code=status.HTTP_200_OK,
):
    return await controller.update_profile(profile_id, profile, db_session)


@router.post(
    "/",
    response_model=ProfileSerializer,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    profile: ProfileSchema,
    db_session: Session = Depends(db.get_db),
):
    return await controller.create_profile(profile, db_session)
