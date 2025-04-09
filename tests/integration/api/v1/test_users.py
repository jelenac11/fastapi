import uuid
import pytest
from models import Base
from tests.utils.asserts import assert_comment_data, assert_post_data, assert_user_data


async def setup_db(db_engine, user, tag, post, comment):
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
        await session.flush()

        comment.post_id = post.id
        comment.user_id = user.id

        session.add(comment)
        await session.commit()

        await session.refresh(post)
        await session.refresh(tag)
        await session.refresh(user)
        await session.refresh(comment)


@pytest.mark.asyncio
async def test_get_user(client, db_engine, user, tag, post, comment):
    # Setup the database
    await setup_db(db_engine, user, tag, post, comment)

    # Test case 1: get user by id without any includes with non-existing id, should return 404
    non_existing_id = uuid.uuid4()
    response = client.get(f"/api/v1/users/{non_existing_id}")
    assert response.status_code == 404

    # Test case 2: get user by id without any includes, should return user
    response = client.get(f"/api/v1/users/{user.id}")
    assert response.status_code == 200
    response_json = response.json()
    assert_user_data(response_json, user)
    assert "posts" not in response_json
    assert "comments" not in response_json

    # Test case 3: get user by id with include comments,posts, should return user with comments (1) and posts (1)
    response = client.get(f"/api/v1/users/{user.id}?include=comments,posts")
    assert response.status_code == 200
    response_json = response.json()
    assert_user_data(response_json, user)
    assert len(response_json["posts"]) == 1
    assert_post_data(response_json["posts"][0], post)
    assert len(response_json["comments"]) == 1
    assert_comment_data(response_json["comments"][0], comment)
