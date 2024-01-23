from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.sql.profile import Profile
from app.models.sql.user import User, UserIn
from app.repository.generic import GenericRepository, GenericSqlRepository


class UserBaseRepository(GenericRepository[User], ABC):
    """Base repository for user entities."""

    @abstractmethod
    async def get_by_username(self, username: EmailStr) -> Optional[User]:
        """Retrieve a user by their username.

        Args:
            username (EmailStr): The username of the user.

        Returns:
            Optional[User]: The user object if found, None otherwise.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_fav_profiles(self, user_id: int) -> Optional[User]:
        """Retrieve a user by their username.

        Args:
            username (EmailStr): The username of the user.

        Returns:
            Optional[User]: The user object if found, None otherwise.
        """
        raise NotImplementedError()


class UserRepository(GenericSqlRepository[User, UserIn], UserBaseRepository):
    """
    Repository class for managing User objects.

    This class provides methods for interacting with the database
    to perform CRUD operations on User entities.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_by_username(self, username: EmailStr) -> Optional[User]:
        query = select(self._model_cls).where(
            self._model_cls.username == username,
            self._model_cls.enabled is True,
        )
        return self._session.exec(query).first()

    async def get_fav_profiles(self, user_id: UUID) -> Optional[List[Profile]]:
        # Get all favoutite profiles for a user
        query = (
            select(self._model_cls)
            .where(
                self._model_cls.id == user_id,
                self._model_cls.enabled is True,
            )
            .join(self._model_cls.favorite_profiles)
        )
        users = await self._session.exec(query)
        user = users.first()
        profiles = user
        return profiles
