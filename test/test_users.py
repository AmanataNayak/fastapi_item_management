from fastapi import status
import pytest
from test.database import client, session


def test_root(client):
    res = client.get('/')
    assert res.json().get('message') == 'Hello, World!'
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize('email, password', [
    ('test@gmail.com', '123'),
    ('try@gmail.com', 'abc')
])
def test_create_user(client, email, password):
    res = client.post('/users/', json={'email': email, 'password': password})
    assert res.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize('email, password', [
    ('test@gmail.com', '123'),
    ('try@gmail.com', 'abc')
])
def test_login(client, email, password):
    res = client.post('/login', data={'username': email, 'password': password})
    assert res.status_code == status.HTTP_200_OK
