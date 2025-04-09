from unittest.mock import MagicMock
from uuid import uuid4
from api.schemas.responses import PostResponse
import pytest

@pytest.fixture
def mock_tag_instance():
    tag = MagicMock()
    tag.id = uuid4()
    tag.name = "testtag"
    return tag

@pytest.fixture
def mock_post_instance(mock_user_instance, mock_tag_instance):
    post = MagicMock()
    post.id = uuid4()
    post.title = "Test Post"
    post.content = "Test content"
    post.status = "draft"
    post.user = mock_user_instance
    post.comments = []
    post.tags = [mock_tag_instance]
    
    post.unloaded = []
    
    return post


@pytest.fixture
def mock_user_instance():
    user = MagicMock()
    user.id = uuid4()
    user.username = "testuser"
    user.email = "testuser@example.com"
    return user


def test_from_orm_safe_for_posts(mock_post_instance, mock_user_instance, mock_tag_instance):
    post_data = PostResponse.from_orm_safe(mock_post_instance)
    
    assert post_data.id == mock_post_instance.id
    assert post_data.title == mock_post_instance.title
    assert post_data.content == mock_post_instance.content
    assert post_data.status == mock_post_instance.status
    assert post_data.user.id == mock_user_instance.id
    assert post_data.user.username == mock_user_instance.username
    assert len(post_data.tags) == 1
    assert post_data.tags[0].id == mock_tag_instance.id
    assert post_data.tags[0].name == mock_tag_instance.name
