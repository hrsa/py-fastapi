import os
from copy import deepcopy

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import get_db
from app.main import app

db_url = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.test_db_name}"


@pytest.fixture(scope='session')
def engine():
    return create_engine(db_url)


@pytest.fixture(scope='module')
def client(engine):
    os.environ["IS_TESTING"] = "True"
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, 'head')

    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    command.downgrade(alembic_cfg, 'base')
    os.environ.pop("IS_TESTING", None)


@pytest.fixture(scope="module")
def authorized_client(client, engine):
    test_name = "Tester of Tests"
    test_email = "test@test.com"
    test_password = "testingpassword"

    client.post('/users/', json={
        "name": test_name,
        "email": test_email,
        "password": test_password})

    res = client.post('/auth/login/', data={
        "username": test_email,
        "password": test_password
    })


    access_token = res.json()["access_token"]

    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    auth_client = TestClient(app)
    auth_client.headers = {**auth_client.headers, 'Authorization': f'Bearer {access_token}'}

    return auth_client


@pytest.fixture(scope='function')  # function scope to get a new session for each test
def db_session(engine):
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = testing_session_local()
    yield session
    # Actions after yield act as teardown for the fixture
    # Close session after each test to roll back any transactions (uncommit changes)
    session.close()
