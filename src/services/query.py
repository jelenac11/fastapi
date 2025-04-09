from typing import Any
from uuid import UUID

from exceptions.custom_exceptions import NotFoundError
from models import Base
from repository.base import BaseRepository


class QueryService:
    def __init__(self, repository: BaseRepository, model: type[Base]) -> None:
        self.repository = repository
        self.model = model

    async def get_many(
        self,
        filters: dict[str, Any] | None = None,
        includes: list[str] | None = None,
    ) -> list[Base]:
        """
        Get posts from the database.

        Args:
            filters (dict): Filters to apply to the query.
            includes (list): Related models to include in the response.

        Returns:
            list[Post]: list of Post objects.

        """
        filters = filters or {}
        includes = includes or []
        return await self.repository.get_data(  # type: ignore
            model=self.model,
            filters=filters,
            includes=includes,
        )

    async def get_one(
        self,
        id: UUID,
        filters: dict[str, Any] | None = None,
        includes: list[str] | None = None,
    ) -> Base | None:
        """
        Get a single post from the database.

        Args:
            id (str): ID of the post to retrieve.
            filters (dict): Filters to apply to the query.
            includes (list): Related models to include in the response.

        Returns:
            Post | None: Post object if found, None otherwise.

        Raises:
            NotFoundError: If the item with the given ID is not found.

        """
        filters = filters or {}
        includes = includes or []

        filters["id"] = id
        item = await self.repository.get_data(
            model=self.model,
            filters=filters,
            includes=includes,
        )

        if not item:
            raise NotFoundError(f"Item of type {self.model.__name__} with ID '{id}' not found.")

        return item[0]
