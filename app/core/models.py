from datetime import datetime
from typing import List, Type, TypeVar
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlmodel import Field, SQLModel

T = TypeVar("T", bound=SQLModel)


def transform_entities(
    entities: List[SQLModel],
    entity_model: Type[T],
) -> List[T]:
    """
    Transforms a list of entities into a list of instances of the specified entity model.

    Args:
        entities (List[SQLModel]): The list of entities to transform.
        entity_model (Type[T]): The entity model class to use for transformation.

    Returns:
        List[T]: The list of transformed entities.

    """
    return [entity_model.model_validate(entity) for entity in entities]


class UUIDModel(SQLModel):
    """
    A base model class that provides a UUID primary key field.

    Attributes:
        uuid (uuid_pkg.UUID): The UUID primary key field.
    """

    uuid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("gen_random_uuid()"),
            "unique": True,
        },
    )


class TimestampModel(SQLModel):
    """
    A base model class that includes timestamp fields for creation and update times.
    """

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)"),
        },
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)"),
            "onupdate": text("current_timestamp(0)"),
        },
    )
