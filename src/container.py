from dependency_injector import containers, providers
from repository.base import BaseRepository
from repository.db_manager import DatabaseManager
from services.post import PostService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.routes.v1.posts",
        ],
    )

    config = providers.Configuration()

    db: DatabaseManager = providers.Singleton(
        DatabaseManager,
        db_connection_str=config.db_url,
    )

    # repositories
    base_repository: BaseRepository = providers.Factory(
        BaseRepository,
        db=db,
    )

    # services
    post_service: PostService = providers.Factory(
        PostService,
        post_repository=base_repository,
    )
