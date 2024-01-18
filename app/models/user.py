""" User model in Pydantic Configuration."""
from typing import List

# Import Pydantic BaseModel and EmailStr
from pydantic import BaseModel, EmailStr

from app.models.profile import ProfileSchema


class UserSchema(BaseModel):
    """User model."""

    # Declare user attributes
    username: EmailStr
    password: str
    created_at: str
    updated_at: str
    # An user can have multiple profiles
    profiles: List[ProfileSchema]
    favorite_profiles: List[ProfileSchema]


class UserSerializer(UserSchema):
    id: int
    # Enabled is a boolean value to determinate logic deletion
    enabled: bool

    class Config:
        from_attributes = True
