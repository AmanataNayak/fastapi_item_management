import pytest
from fastapi.testclient import TestClient
from app.main import app
from fastapi import status

client = TestClient(app)


def test_root():
    res = client.get('/')
    assert res.json().get('message') == 'Hello, World!'
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize('email, password',[
    ('pavan@gmail.com','123'),
    ('rimjhim@gmail.com','rim')
])
def test_create_user(email, password):
    res = client.post('/users/',json={'email':email, 'password': password})
    print(res.json())
    assert res.status_code == status.HTTP_201_CREATED