import uuid
import pytest
from models import Base
from tests.utils.asserts import (
    assert_comment_data,
    assert_post_data,
    assert_tag_data,
    assert_user_data,
)


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


@pytest.mark.asyncio
async def test_get_posts(client, db_engine, user, tag, post, comment):
    # Setup the database
    await setup_db(db_engine, user, tag, post, comment)

    # Test case 1: get posts without any filters and includes, should return post
    response = client.get("/api/v1/posts")
    assert response.status_code == 200

    response_json = response.json()
    assert isinstance(response_json, list)
    assert len(response_json) == 1
    assert_post_data(response_json[0], post)
    assert "user" not in response_json[0]

    # Test case 2: get posts with status draft, should return 1 post
    response = client.get("/api/v1/posts?status=draft")
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list)
    assert len(response_json) == 1
    assert len(response_json) == 1
    assert_post_data(response_json[0], post)

    # Test case 3: get posts with status published, should return 0 posts
    response = client.get("/api/v1/posts?status=published")
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list)
    assert len(response_json) == 0

    # Test case 4: get posts with status draft and include tags and user, should return 1 post with 1 tag and user
    response = client.get("/api/v1/posts?status=draft&include=tags,user")
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list)
    assert len(response_json) == 1

    assert_post_data(response_json[0], post)
    assert len(response_json[0]["tags"]) == 1
    assert_tag_data(response_json[0]["tags"][0], tag)
    assert_user_data(response_json[0]["user"], user)


@pytest.mark.asyncio
async def test_get_post(client, db_engine, user, tag, post, comment):
    # Setup the database
    await setup_db(db_engine, user, tag, post, comment)

    # Test case 1: get post by id without any includes with non-existing id, should return 404
    non_existing_id = uuid.uuid4()
    response = client.get(f"/api/v1/posts/{non_existing_id}")
    assert response.status_code == 404

    # Test case 2: get post by id without any includes, should return post
    response = client.get(f"/api/v1/posts/{post.id}")
    assert response.status_code == 200
    response_json = response.json()
    assert_post_data(response_json, post)
    assert "user" not in response_json
    assert "tags" not in response_json
    assert "comments" not in response_json

    # Test case 3: get post by id with include tags, should return post with tags (1)
    response = client.get(f"/api/v1/posts/{post.id}?include=tags")
    assert response.status_code == 200
    response_json = response.json()
    assert_post_data(response_json, post)
    assert len(response_json["tags"]) == 1
    assert_tag_data(response_json["tags"][0], tag)

    # Test case 4: get post by id with include user, tags, comments, should return post with user, tags (1) and comments (1)
    response = client.get(f"/api/v1/posts/{post.id}?include=user,tags,comments")
    assert response.status_code == 200
    response_json = response.json()
    assert_post_data(response_json, post)
    assert_user_data(response_json["user"], user)
    assert len(response_json["tags"]) == 1
    assert_tag_data(response_json["tags"][0], tag)
    assert len(response_json["comments"]) == 1
    assert_comment_data(response_json["comments"][0], comment)
