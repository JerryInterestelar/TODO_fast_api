import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import table_registry
from fast_zero.security import get_password_hash
from tests.factories import UserFactory


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture()
def session(engine):
    # TODO
    # Estudar melhor esse processo
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        # TODO
        # Estudar essa palavra
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def user(session):
    pwd = 'test_password'
    user = UserFactory(
        password=get_password_hash(pwd),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # Monkey patch

    return user


@pytest.fixture()
def other_user(session):
    pwd = 'test_password'
    user = UserFactory(
        password=get_password_hash(pwd),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # Monkey patch

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        'auth/token',
        data={
            'username': user.username,
            'password': user.clean_password,
        },
    )

    return response.json()['access_token']
