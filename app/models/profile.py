"""User Profile Model Pydantic Configuration."""
from pydantic import BaseModel


class ProfileSchema(BaseModel):
    """Profile model."""

    int: int
    created_at: str
    updated_at: str
    enabled: bool
    name: str
    description: str


class ProfileSerializer(ProfileSchema):
    id: int

    class Config:
        from_attributes = True
