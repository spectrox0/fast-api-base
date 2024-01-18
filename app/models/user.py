""" User model in Pydantic Configuration."""
from typing import List

# Import Pydantic BaseModel and EmailStr
from pydantic import BaseModel, EmailStr

from app.models.profile import ProfileSchema


class UserSchema(BaseModel):
    """User model."""

    # Declare user attributes
    email: EmailStr
    enabled: bool
    created_at: str
    updated_at: str
    # An user can have multiple profiles
    profiles: List[ProfileSchema]
    favorite_profiles: List[ProfileSchema]


class UserSerializer(UserSchema):
    id: int

    class Config:
        from_attributes = True
