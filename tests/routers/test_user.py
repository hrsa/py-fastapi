from app.models import User

test_name = "Tester of Tests"
test_email = "test@test.com"
test_password = "testingpassword"


def test_create_user(client, db_session):
    res = client.post('/users/', json={
        "name": test_name,
        "email": test_email,
        "password": test_password})
    assert res.status_code == 201
    user = db_session.query(User).filter_by(email=test_email).first()
    assert user.name == test_name
    assert user.id == 1

    res = client.post('/users/', json={
        "name": test_name,
        "email": test_email,
        "password": test_password})
    assert res.status_code == 403


def test_get_user(client, db_session):
    res = client.get('/users/1')
    assert res.status_code == 200
    user = res.json()
    assert user["name"] == test_name
    assert user["email"] == test_email

    res = client.get('/users/2')
    assert res.status_code == 404

def test_auth(client, db_session):
    res = client.post('/auth/login/', data={
        "username": test_email,
        "password": test_password
    })
    assert res.status_code == 200
    assert res.json()["access_token"] is not None

    res = client.post('/auth/login/', data={
        "username": test_email,
        "password": test_password + "failme"
    })

    assert res.status_code == 403
    assert "access_token" not in res.json()
