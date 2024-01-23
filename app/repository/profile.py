from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.sql.profile import Profile, ProfileBase
from app.repository.generic import GenericSqlRepository


class ProfileRepository(GenericSqlRepository[Profile], ProfileBase):
    """
    Repository class for managing profiles in the database.

    Args:
        session (AsyncSession): The async session object for database operations.

    Attributes:
        session (AsyncSession): The async session object for database operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Profile)
