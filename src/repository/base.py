import logging
from typing import Any, Type
from models.base import Base
from repository.db_manager import DatabaseManager
from sqlalchemy import select
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)


class BaseRepository:
    def __init__(self, db: DatabaseManager) -> None:
        self.session_factory = db.session

    async def get_data(
        self, model: Type[Base], filters: dict[str, Any] = None, includes: list[str] = None
    ) -> list[Base]:
        """
        Generic query function for filtering and including related models.
        """
        query = select(model)

        # Apply filters dynamically
        if filters:
            for key, value in filters.items():
                column = getattr(model, key, None)
                if column:
                    query = query.filter(column == value)
                else:
                    logger.warning(f"Column {key} not found in model {model.__name__}")

        # Apply related table joins dynamically
        if includes:
            for relation in includes:
                relation_attr = getattr(model, relation, None)
                if relation_attr:
                    query = query.options(selectinload(relation_attr))
                else:
                    logger.warning(f"Relation {relation} not found in model {model.__name__}")

        async with self.session_factory() as session:
            result = await session.execute(query)

            return result.scalars().all()  # type: ignore
