"""User Profile Model Pydantic Configuration."""
from pydantic import BaseModel


class ProfileSchema(BaseModel):
    """Profile model."""

    created_at: str
    updated_at: str
    # Enabled is a boolean value to determinate logic deletion
    enabled: bool
    name: str
    description: str


class ProfileSerializer(ProfileSchema):
    id: int

    class Config:
        from_attributes = True
