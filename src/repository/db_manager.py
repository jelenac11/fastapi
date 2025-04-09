import logging
from asyncio import current_task
from collections.abc import Callable
from contextlib import (
    AbstractAsyncContextManager,
    asynccontextmanager,
)

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database manager to create engine to manage database interactions."""

    def __init__(self, db_connection_str: str) -> None:
        """
        Database manager to create database engine and session factory.

        Args:
            db_connection_str (str): Database connection string

        """
        self._engine = create_async_engine(
            db_connection_str,
            pool_pre_ping=True,
            pool_recycle=600,
        )
        self._session_maker = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )
        self._session_factory = async_scoped_session(
            self._session_maker,
            scopefunc=current_task,
        )

    @asynccontextmanager  # type: ignore
    async def session(self) -> Callable[..., AbstractAsyncContextManager]:  # type: ignore
        """Gets a session from the session factory and closes it after use."""
        async_session: AsyncSession = self._session_factory()
        try:
            yield async_session
        except Exception:
            logger.exception("Session rollback because of exception")
            await async_session.rollback()
            raise
        finally:
            await async_session.close()

    @property
    def engine(self) -> AsyncEngine:
        return self._engine
