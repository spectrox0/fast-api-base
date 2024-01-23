from abc import ABC

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.sql.profile import Profile
from app.repository.generic import GenericRepository, GenericSqlRepository


class ProfileBaseRepository(GenericRepository[Profile], ABC):
    """
    Repository class for managing profiles in the database.

    Args:
        session (AsyncSession): The async session object for database operations.

    Attributes:
        session (AsyncSession): The async session object for database operations.
    """


class ProfileRepository(GenericSqlRepository[Profile], ProfileBaseRepository):
    """
    Repository class for managing profiles in the database.

    Args:
        session (AsyncSession): The async session object for database operations.

    Attributes:
        session (AsyncSession): The async session object for database operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Profile)
