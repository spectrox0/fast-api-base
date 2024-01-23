from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from sqlmodel import SQLModel, and_, select
from sqlmodel import update as update_sql
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import SelectOfScalar

from app.core.models import TableBase

T = TypeVar("T", bound=TableBase)
U = TypeVar("U", bound=SQLModel)


# GenericRepository is a generic class that implements the basic CRUD
class GenericRepository(Generic[T, U], ABC):
    """
    A generic repository interface for CRUD operations on models.

    This class provides abstract methods for retrieving, listing, adding,
    updating, and deleting models.

    Attributes:
        T: The type of the model.

    """

    @abstractmethod
    async def get_by_id(self, model_id: Union[int, str]) -> Optional[T]:
        """
        Retrieve a model by its ID.

        Args:
            model_id (Union[int, str]): The ID of the model.

        Returns:
            Optional[T]: The retrieved model, or None if not found.
        """
        raise NotImplementedError()

    @abstractmethod
    async def list(self, **filters) -> List[T]:
        """
        List models based on the provided filters.

        Args:
            **filters: Additional filters to apply to the query.

        Returns:
            List[T]: A list of models that match the filters.
        """
        raise NotImplementedError()

    @abstractmethod
    async def add(self, record: Type[U]) -> T:
        """
        Add a new model to the repository.

        Args:
            record (T): The model to add.

        Returns:
            T: The added model.
        """
        raise NotImplementedError()

    @abstractmethod
    async def update(
        self,
        model_id: Union[str, int, UUID],
        record: Type[U],
    ) -> T:
        """
        Update an existing model in the repository.

        Args:
            record (T): The model to update.

        Returns:
            T: The updated model.
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, model_id: Union[int, str, UUID]) -> None:
        """
        Delete a model from the repository.

        Args:
            model_id (Annotated[int, str]): The ID of the model to delete.
        """
        raise NotImplementedError()


class GenericSqlRepository(GenericRepository[T, U], ABC):
    def __init__(self, session: AsyncSession, model_cls: T) -> None:
        self._session = session
        self._model_cls = model_cls

    def _construct_get_stmt(self, model_id: str) -> SelectOfScalar:
        """
        Constructs the SQL statement for retrieving a model by its ID.

        Args:
            model_id (str): The ID of the model.

        Returns:
            SelectOfScalar: The constructed SQL statement.
        """
        stmt = select(self._model_cls).where(
            self._model_cls.id == model_id,
            self._model_cls.enabled is True,
        )
        return stmt

    async def get_by_id(self, model_id: str) -> Optional[T]:
        """
        Retrieves a model by its ID.

        Args:
            model_id (str): The ID of the model.

        Returns:
            Optional[T]: The retrieved model, or None if not found.
        """
        stmt = self._construct_get_stmt(model_id)
        return await self._session.exec(stmt).first()

    async def _construct_list_stmt(self, **filters) -> SelectOfScalar:
        """Creates a SELECT query for retrieving a multiple records.

        Raises:
            ValueError: Invalid column name.

        Returns:
            SelectOfScalar: SELECT statement.
        """
        stmt = select(self._model_cls)
        where_clauses = []
        for c, v in filters.items():
            if not hasattr(self._model_cls, c):
                raise ValueError(f"Invalid column name {c}")
            where_clauses.append(getattr(self._model_cls, c) == v)

        if len(where_clauses) == 1:
            stmt = stmt.where(where_clauses[0])
        elif len(where_clauses) > 1:
            stmt = stmt.where(and_(*where_clauses, **{}))
        return stmt

    async def list(self, **filters) -> List[T]:
        stmt = self._construct_list_stmt(**{**filters, "enabled": True})
        return await self._session.exec(stmt).all()

    async def add(self, record: T) -> T:
        self._session.add(record)
        # await self._session.flush()
        # await self._session.refresh(record)
        await self._session.commit()
        return record

    async def update(
        self,
        model_id: Union[str, int, UUID],
        record: U,
    ) -> T:
        query = (
            update_sql(self._model_cls)
            .where(self._model_cls.id == model_id)
            .values(**record.model_dump())
            .returning(self._model_cls)
        )
        record = await self._session.exec(query).first()
        await self._session.commit()
        return record

    async def delete(self, model_id: Union[int, str, UUID]) -> bool:
        query = (
            update_sql(self._model_cls)
            .where(self._model_cls.id == model_id)
            .values(enabled=False)
            .returning(self._model_cls)
        )
        res = self._session.exec(query)
        await self._session.commit()
        return res is not None
