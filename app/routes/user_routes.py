from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.controllers.user_controller as controller
from app.models.user import UserSchema, UserSerializer
from config.database import db

module = "users"
router = APIRouter(
    prefix=f"/{module}",
)


@router.post("/")
async def create_user(
    user: UserSchema,
    db_session: Session = Depends(db.get_db),
) -> UserSerializer:
    return controller.create_user(user, db_session)


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    db_session=Depends(db.get_db),
) -> UserSerializer:
    user_id = int(user_id)
    user = await UserSchema.get(db_session, id=user_id)
    return user


@router.get("/")
async def get_all_users(db_session=Depends(db.get_db)) -> List[UserSerializer]:
    users = await UserSchema.get_all(db_session)
    return users


@router.put("/{id}")
async def update(
    user_id: str,
    user: UserSchema,
    db_session=Depends(db.get_db),
) -> UserSerializer:
    user_id = int(user_id)
    user = await UserSchema.update(db_session, id=user_id, **user.model_dump())
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: str, db_session=Depends(db.get_db)) -> bool:
    user_id = int(user_id)
    return await UserSchema.delete(db_session, id=user_id)
