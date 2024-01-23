from abc import ABC, abstractmethod
from typing import Callable

from sqlmodel.ext.asyncio.session import AsyncSession

from app.repository.profile import ProfileBaseRepository, ProfileRepository
from app.repository.user import UserBaseRepository, UserRepository


class UnitOfWorkBase(ABC):
    users: UserBaseRepository
    profiles: ProfileBaseRepository

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError()


class UnitOfWork(UnitOfWorkBase):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session = None

    def __enter__(self):
        self._session = self._session_factory()
        self.users = UserRepository(self._session)
        self.profiles = ProfileRepository(self._session)
        return super().__enter__()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
