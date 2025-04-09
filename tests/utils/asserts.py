def assert_post_data(post_data, expected_post):
    assert post_data["id"] == str(expected_post.id)
    assert post_data["title"] == expected_post.title
    assert post_data["content"] == expected_post.content
    assert post_data["status"] == expected_post.status


def assert_tag_data(tag_data, expected_tag):
    assert tag_data["id"] == str(expected_tag.id)
    assert tag_data["name"] == expected_tag.name


def assert_comment_data(comment_data, expected_comment):
    assert comment_data["id"] == str(expected_comment.id)
    assert comment_data["content"] == expected_comment.content


def assert_user_data(user_data, expected_user):
    assert user_data["id"] == str(expected_user.id)
    assert user_data["username"] == expected_user.username
