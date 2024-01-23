from typing import Any, Dict, List, Optional, Set

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.core.models import TableBase, UUIDModel
from app.models.sql.profile import Profile


class UserBase(SQLModel):
    """Base model for a user."""

    username: EmailStr = Field(unique=True)


class UserIn(UserBase):
    """Model for creating a user."""

    password: str = Field()


class UserOut(UserBase, UUIDModel):
    """Model for reading a user."""


class User(UserBase, TableBase, table=True):
    """
    Represents a user in the system.

    Attributes:
        created_at (datetime): The timestamp when the user was created.
        id (str): The unique identifier of the user.
        username (str): The email address of the user.
        profiles (List[Profile]): The profiles associated with the user.
        favorite_profiles (List[Profile]): The favorite profiles of the user.
    """

    # The table name in the database
    __tablename__ = "users"
    password: str = Field()
    # Relationship with the Profile model
    profiles: List[Profile] = Relationship(back_populates="user")

    @property
    def favorite_profiles(self) -> List["Profile"]:
        return [profile for profile in self.profiles if profile.favorite]

    def dict(
        self,
        by_alias: bool = False,
        exclude_none: bool = False,
        exclude: Optional[Set[str]] = None,
        include: Optional[Set[str]] = None,
    ) -> Dict[str, Any]:
        model_dict = super().model_dump(
            by_alias=by_alias,
            exclude_none=exclude_none,
            exclude=exclude,
            include=include,
        )
        model_dict["favorite_profiles"] = [
            profile.model_dump() for profile in self.favorite_profiles
        ]
        return model_dict
