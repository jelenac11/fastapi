import pytest
import pytest_asyncio
import asyncio
import os
import sys
from fastapi.testclient import TestClient

sys.path.append("./src")

from main import app
from models import Base, User, Tag, Post, Comment, PostStatus
from repository.db_manager import DatabaseManager


@pytest.fixture
def user():
    return User(username="johndoe", email="johndoe@example.com")


@pytest.fixture
def tag():
    return Tag(name="Python")


@pytest.fixture
def post():
    return Post(
        title="Learning Python",
        content="Python is a versatile programming language.",
        status=PostStatus.DRAFT,
    )


@pytest.fixture
def comment():
    return Comment(
        content="Great post! Really informative.",
    )


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    db_url = os.environ["DB_URL"]
    db_manager = DatabaseManager(db_url)

    # Create all tables once
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield db_manager

    # Drop tables once after all tests
    # async with db_manager.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)

    await db_manager.engine.dispose()


@pytest.fixture(scope="session")
def client(db_engine):
    app.container.db_manager = db_engine
    with TestClient(app) as c:
        yield c
