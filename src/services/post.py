from typing import Any
from models.post import Post
from repository.base import BaseRepository


class PostService:
    def __init__(self, post_repository: BaseRepository) -> None:
        self.post_repository = post_repository

    async def get(self, filters: dict[str, Any] = {}, includes: list[str] = []) -> list[Post]:
        """Get posts from the database.
        Args:
            filters (dict): Filters to apply to the query.
            includes (list): Related models to include in the response.
        Returns:
            list[Post]: List of Post objects.
        """
        return await self.post_repository.get_data(  # type: ignore
            model=Post,
            filters=filters,
            includes=includes,
        )
