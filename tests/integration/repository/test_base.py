import pytest
from models import Base, Tag, User, Post, PostStatus
from repository.base import BaseRepository


@pytest.fixture
def base_repository(db_engine):
    return BaseRepository(db_engine)


@pytest.mark.asyncio
async def test_get_data(base_repository, db_engine, post, user, tag, comment):
    # Setup: Create test data
    async with db_engine.session() as session:
        # Delete all existing data
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()

        session.add_all([user, tag])
        await session.flush()

        post.user_id = user.id
        post.tags.append(tag)

        session.add(post)
        await session.flush()  # NOW post.id is available

        # Now we can safely assign post_id
        comment.post_id = post.id
        comment.user_id = user.id

        session.add(comment)
        await session.commit()

        await session.refresh(post)
        await session.refresh(tag)
        await session.refresh(user)
        await session.refresh(comment)

    # Test case 1: Get archived posts, should return empty list
    result = await base_repository.get_data(
        Post, filters={"status": PostStatus.ARCHIVED}, includes=["user", "tags"]
    )

    assert result == []

    # Test case 2: Get draft posts with user, should return 1 post with user
    result = await base_repository.get_data(
        Post, filters={"status": PostStatus.DRAFT}, includes=["user"]
    )
    assert result
    assert len(result) == 1
    assert result[0].status == PostStatus.DRAFT
    assert result[0].user is not None
    assert result[0].user.username == user.username
    assert result[0].user.id == user.id
    assert result[0].title == post.title

    # Test case 3: Get tags, no filters, should return all tags (1)
    result = await base_repository.get_data(
        Tag,
    )
    assert result
    assert len(result) == 1
    assert result[0].name == tag.name
    assert result[0].id == tag.id

    # Test case 4: Get users, no filters, includes posts, should return all users (1) with their posts (1)
    result = await base_repository.get_data(User, includes=["posts"])
    assert result
    assert len(result) == 1
    assert result[0].username == user.username
    assert result[0].id == user.id
    assert result[0].posts
    assert len(result[0].posts) == 1
    assert result[0].posts[0].title == post.title
    assert result[0].posts[0].id == post.id
