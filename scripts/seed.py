import os
import sys
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError("DB_URL environment variable is not set.")

# Fix pathing for module imports
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root / "src"))

from models import Base, Post, User, Comment, Tag, PostStatus

# Create async engine and session
engine = create_async_engine(DB_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def seed_db() -> None:
    async with async_session() as session:
        async with session.begin():
            # Creating users
            user1 = User(username="johndoe", email="johndoe@example.com")
            user2 = User(username="janedoe", email="janedoe@example.com")

            # Creating tags
            tag1 = Tag(name="Python")
            tag2 = Tag(name="FastAPI")
            tag3 = Tag(name="SQLAlchemy")

            # Creating posts
            post1 = Post(
                title="Introduction to Python",
                content="This is a post about Python programming.",
                status=PostStatus.DRAFT,
                user=user1,
            )

            post2 = Post(
                title="Advanced FastAPI Concepts",
                content="A detailed post about advanced FastAPI features.",
                status=PostStatus.PUBLISHED,
                user=user2,
            )

            # Creating comments
            comment1 = Comment(
                content="Great post! Really informative.", user=user1, post=post1
            )
            comment2 = Comment(content="I love FastAPI!", user=user2, post=post2)

            # Add tags to posts
            post1.tags.extend([tag1, tag2])
            post2.tags.extend([tag2, tag3])

            # Add all to session
            session.add_all(
                [user1, user2, tag1, tag2, tag3, post1, post2, comment1, comment2]
            )

    print("Database seeded successfully!")


async def create_db_and_seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await seed_db()


if __name__ == "__main__":
    asyncio.run(create_db_and_seed())
