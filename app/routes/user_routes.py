from typing import List

from fastapi import Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

import app.controllers.user_controller as controller
from app.models.user import UserSchema, UserSerializer
from app.utils.router import get_api_router
from config.database import get_session

router = get_api_router("users")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSerializer,
    tags=["users"],
)
async def create_user(
    user: UserSchema,
    db_session: AsyncSession = Depends(get_session),
) -> UserSerializer:
    """
    Create a new user.

    Args:
        user (UserSchema): The user data to be created.
        db_session (Session, optional): The database session. Defaults to Depends(db.get_db).

    Returns:
        UserSerializer: The serialized user object.

    """
    return controller.create_user(user, db_session)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(
    user_id: str,
    db_session: AsyncSession = Depends(get_session),
    tags=["users"],
) -> UserSerializer:
    """
    Retrieve a user by their ID.

    Args:
        user_id (str): The ID of the user.
        db_session: The database session.

    Returns:
        UserSerializer: The serialized user object.
    """
    user_id = int(user_id)
    user = await UserSchema.get(db_session, id=user_id)
    return user


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
async def get_all_users(
    db_session: AsyncSession = Depends(get_session),
) -> List[UserSerializer]:
    """
    Retrieve all users from the database.

    Parameters:
        db_session (DatabaseSession): The database session.

    Returns:
        List[UserSerializer]: A list of user objects serialized as UserSerializer.

    """
    return []


@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
)
async def update(
    user_id: str,
    user: UserSchema,
    db_session: AsyncSession = Depends(get_session),
) -> UserSerializer:
    user_id = int(user_id)
    user = await UserSchema.update(db_session, id=user_id, **user.model_dump())
    return user


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: str,
    db_session: AsyncSession = Depends(get_session),
) -> bool:
    """
    Delete a user from the database.

    Args:
        user_id (str): The ID of the user to be deleted.
        db_session: The database session.

    Returns:
        bool: True if the user is successfully deleted, False otherwise.
    """
    user_id = int(user_id)
    return await UserSchema.delete(db_session, id=user_id)
