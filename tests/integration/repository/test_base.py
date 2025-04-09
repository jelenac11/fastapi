import pytest
from repository.base import BaseRepository


@pytest.fixture()
def repository():
    return BaseRepository()

