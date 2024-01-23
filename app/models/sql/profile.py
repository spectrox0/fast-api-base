""" SQLModel for the Profile model. """

from sqlmodel import Field, SQLModel

from app.core.models import TableBase, UUIDModel


class ProfileBase(SQLModel):
    """Base model for a profile."""

    name: str = Field()
    description: str = Field()
    user_id: str = Field(foreign_key="users.id")


class ProfileIn(ProfileBase):
    """Model for creating a profile."""


class ProfileOut(ProfileBase, UUIDModel):
    """Model for reading a profile."""


class Profile(ProfileBase, TableBase, table=True):
    """
    Represents a user profile.

    Attributes:
        id (str): The unique identifier for the profile.
        name (str): The name of the profile.
        description (str): The description of the profile.
        user_id (str): The foreign key referencing the user's ID.
    """

    __tablename__ = "profiles"
    user_id: str = Field(foreign_key="users.id")
    favorite: bool = Field(default=False)
