from dependency_injector import containers, providers

from models import Post, User
from repository.base import BaseRepository
from repository.db_manager import DatabaseManager
from services.query import QueryService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.routes.v1.posts",
            "api.routes.v1.users",
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
    post_service: QueryService = providers.Factory(
        QueryService,
        repository=base_repository,
        model=Post,
    )

    user_service: QueryService = providers.Factory(
        QueryService,
        repository=base_repository,
        model=User,
    )
