""" User model for SQL database."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression as sql

from app.models.sql.profile import favorite_profiles
from config.database import Base


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        created_at (DateTime): The timestamp when the user was created.
        id (String): The unique identifier of the user.
        email (String): The email address of the user.
        profiles (List[Profile]): The profiles associated with the user.
        favorite_profiles (List[Profile]): The favorite profiles of the user.
    """

    __tablename__ = "users"
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    id = Column(String, primary_key=True)
    username = Column(String, unique=True)
    profiles = relationship("Profile", backref="user")
    favorite_profiles = relationship("Profile", secondary=favorite_profiles)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_name={self.full_name}, "
            f")>"
        )

    @classmethod
    async def create(cls, db, **kwargs) -> "User":
        """
        Create a new user in the database.

        Args:
            db: The database connection.
            **kwargs: Additional keyword arguments representing the user attributes.

        Returns:
            The created user object.

        """
        query = (
            sql.insert(cls)
            .values(id=str(uuid4()), **kwargs)
            .returning(cls.id, cls.full_name)
        )
        users = await db.execute(query)
        await db.commit()
        return users.first()

    @classmethod
    async def update(cls, db, user_id, **kwargs) -> "User":
        query = (
            sql.update(cls)
            .where(cls.id == user_id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
            .returning(cls.id, cls.full_name)
        )
        users = await db.execute(query)
        await db.commit()
        return users.first()

    @classmethod
    async def get(cls, db, id) -> "User":
        query = sql.select(cls).where(cls.id == id)
        users = await db.execute(query)
        (user,) = users.first()
        return user

    @classmethod
    async def get_all(cls, db) -> list["User"]:
        query = sql.select(cls)
        users = await db.execute(query)
        users = users.scalars().all()
        return users

    @classmethod
    async def delete(cls, db, id) -> bool:  # noqa: A002
        query = (
            sql.delete(cls)
            .where(cls.id == id)
            .returning(
                cls.id,
                cls.full_name,
            )
        )
        await db.execute(query)
        await db.commit()
        return True
