import pytest

from app import schemas
from app.models import Post
from pythonray import ray

from app.models import User

test_name = "Tester of Tests"
test_email = "test@test.com"
test_password = "testingpassword"


def test_create_post(client, db_session, authorized_client):
    res = authorized_client.post('/posts/', json={
        "title": "Test Post",
        "content": "This is a test post"
    })
    post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert post.title == "Test Post"
    assert post.content == "This is a test post"
    assert post.author.name == test_name
    assert post.author.email == test_email

    res = client.post('/posts/', json={
        "title": "Test Post",
        "content": "This is a test post"
    })
    assert res.status_code == 401


def test_get_posts(client, db_session):
    new_post = Post(title="Second Post", author_id=1, content="Test content", published=True,
                    rating=5)
    db_session.add(new_post)
    db_session.commit()

    res = client.get('/posts/', params={})
    assert res.status_code == 200

    first_post = schemas.PostResponse(**res.json()[0])

    assert first_post.title == "Test Post"
    assert first_post.content == "This is a test post"
    assert first_post.rating is None
    assert first_post.author.name == test_name
    assert first_post.author.email == test_email

    second_post = schemas.PostResponse(**res.json()[1])

    assert second_post.title == "Second Post"
    assert second_post.content == "Test content"
    assert second_post.rating == 5
    assert second_post.author.name == test_name
    assert second_post.author.email == test_email


def test_get_my_posts(client, db_session, authorized_client):
    res = client.get('/posts/my_posts')
    assert res.status_code == 401

    res = authorized_client.get('/posts/my_posts')

    assert res.status_code == 200
    first_post = schemas.PostBase(**res.json()[0])

    assert first_post.title == "Test Post"
    assert first_post.content == "This is a test post"
    assert first_post.rating is None

    second_post = schemas.PostBase(**res.json()[1])

    assert second_post.title == "Second Post"
    assert second_post.content == "Test content"
    assert second_post.rating == 5


def test_get_post(client):
    res = client.get('/posts/1')
    assert res.status_code == 200

    first_post = schemas.PostResponse(**res.json())

    assert first_post.title == "Test Post"
    assert first_post.content == "This is a test post"
    assert first_post.rating is None
    assert first_post.author.name == test_name
    assert first_post.author.email == test_email

    res = client.get('/posts/2')
    assert res.status_code == 200

    second_post = schemas.PostResponse(**res.json())

    assert second_post.title == "Second Post"
    assert second_post.content == "Test content"
    assert second_post.rating == 5
    assert second_post.author.name == test_name
    assert second_post.author.email == test_email


def test_edit_post(client, db_session, authorized_client):
    edit_data = {
        "title": "Edited post",
        "content": "I edited this post"
    }

    res = client.put('/posts/1', json=edit_data)
    assert res.status_code == 401

    res = authorized_client.put('/posts/1', json=edit_data)

    assert res.status_code == 200

    updated_post = schemas.PostResponse(**res.json())

    assert updated_post.id == 1
    assert updated_post.title == "Edited post"
    assert updated_post.content == "I edited this post"


def test_delete_post(client, db_session, authorized_client):
    res = client.delete('/posts/1')
    assert res.status_code == 401

    res = authorized_client.delete('/posts/1')

    assert res.status_code == 204
    assert db_session.query(Post).filter(Post.id == 1).first() is None


def test_vote(client, db_session, authorized_client):
    res = client.get('/posts/2')
    assert res.json()["likes"] == 0

    res = client.post("/votes/", json={"post_id": 2, "value": 1})
    assert res.status_code == 401

    res = authorized_client.post("/votes/", json={"post_id": 2, "value": 1})
    assert res.status_code == 200

    res = authorized_client.post("/votes/", json={"post_id": 2, "value": 1})
    assert res.status_code == 409

    res = client.get('/posts/2')
    assert res.json()["likes"] == 1

    res = client.post("/votes/", json={"post_id": 2, "value": 0})
    assert res.status_code == 401

    res = authorized_client.post("/votes/", json={"post_id": 2, "value": 0})
    assert res.status_code == 200

    res = authorized_client.post("/votes/", json={"post_id": 2, "value": 0})
    assert res.status_code == 409

    res = client.get('/posts/2')
    assert res.json()["likes"] == 0
