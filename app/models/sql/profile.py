""" SQLModel for the Profile model. """

from sqlmodel import Field, SQLModel

from app.core.models import UUIDModel


class ProfileBase(SQLModel):
    """Base model for a profile."""

    name: str = Field()
    description: str = Field()


class ProfileIn(ProfileBase):
    """Model for creating a profile."""

    user_id: str = Field()


class ProfileOut(ProfileBase, UUIDModel):
    """Model for reading a profile."""


class Profile(SQLModel, table=True):
    """
    Represents a user profile.

    Attributes:
        id (str): The unique identifier for the profile.
        name (str): The name of the profile.
        description (str): The description of the profile.
        user_id (str): The foreign key referencing the user's ID.
    """

    __tablename__ = "profiles"
    id: str = Field(primary_key=True)
    name: str = Field()
    description: str = Field()
    enabled: bool = Field(default=True)
    user_id: str = Field(foreign_key="users.id")
    favorite: bool = Field(default=False)
