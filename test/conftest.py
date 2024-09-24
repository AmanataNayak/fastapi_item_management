import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import setting
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app.models import Item

SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    user_data = {"email": "amanata@gmail.com",
                 "password": "123"}

    response = client.post('/users/', json=user_data)
    assert response.status_code == status.HTTP_201_CREATED

    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_items(test_user, session):
    item_data = [
        {
            'name': 'Cat',
            'price': 22,
            'file_path': '/Users/amanatanayak/Desktop/cat.jpeg',
            'owner_id': test_user['id']
        },
        {
            'name': 'Dog',
            'price': 30,
            'file_path': '/Users/amanatanayak/Downloads/dog.png',
            'owner_id': test_user['id']
        },
        {
            'name': 'TV',
            'price': 30000,
            'file_path': '/Users/amanatanayak/Desktop/a.jpeg',
            'owner_id': test_user['id']
        }
    ]

    def create_item_model(item: dict):
        return Item(**item)

    item_map = map(create_item_model, item_data)
    items = list(item_map)

    session.add_all(items)
    session.commit()

    items = session.query(Item).all()

    return items
