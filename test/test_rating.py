import pytest
from test.conftest import authorized_client, test_items, test_rate
import random
from fastapi import status


def test_rate_on_item(authorized_client, test_items):
    response = authorized_client.post('/rate', json={'item_id': test_items[0].id, 'rating': random.randint(1, 5)})
    assert response.status_code == status.HTTP_201_CREATED


def test_rate_twice_on_item(authorized_client, test_items, test_rate):
    response = authorized_client.post('/rate', json={'item_id': test_items[0].id, 'rating': random.randint(1, 5)})
    assert response.status_code == status.HTTP_409_CONFLICT


def test_rate_not_exist(authorized_client):
    response = authorized_client.post('/rate', json={'item_id': 2000, 'rating': random.randint(1, 5)})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_rate(client, test_items):
    response = client.post('/rate', json={'item_id': test_items[0].id, 'rating': random.randint(1, 5)})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
