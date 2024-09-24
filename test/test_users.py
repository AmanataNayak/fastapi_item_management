from fastapi import status
import pytest
from test.conftest import client, session, test_user


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


def test_login(client, test_user):
    res = client.post('/login', data={'username': test_user['email'], 'password': test_user['password']})
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize('email,password, status_code', [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post('/login', data={'username': email, 'password': password})
    assert response.status_code == status_code
