import pytest
from test.conftest import authorized_client, client, test_items
from fastapi import status


# Create
def test_create_items(authorized_client):
    item_data = {'name': 'cat', 'price': 20}
    with open('/Users/amanatanayak/Desktop/a.png', 'rb') as image_file:
        response = authorized_client.post(
            '/items/',
            data={
                "name": item_data['name'],
                "price": item_data['price']
            },
            files={
                "file": ("cat.jpeg", image_file, "image/jpeg")
            }
        )

    assert response.status_code == status.HTTP_201_CREATED


def test_create_item_invalid_date(authorized_client):
    item_data = {'name': 'TV'}
    with open("/Users/amanatanayak/Desktop/a.png", "rb") as image_file:
        response = authorized_client.post(
            '/items/',
            data={
                "name": item_data['name'],
            },
            files={
                "file": ("cat.jpeg", image_file, "image/jpeg")
            }
        )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_item_unauthorized(client):
    item_data = {'name': 'cat', 'price': 20}
    with open('/Users/amanatanayak/Desktop/a.png', 'rb') as image_file:
        response = client.post(
            '/items/',
            data={
                "name": item_data['name'],
                "price": item_data['price']
            },
            files={
                "file": ("cat.jpeg", image_file, "image/jpeg")
            }
        )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_item_with_invalid_file_type(authorized_client):
    item_data = {'name': 'cat', 'price': 20}
    with open('/Users/amanatanayak/Desktop/Itinerary.pdf', 'rb') as image_file:
        response = authorized_client.post(
            '/items/',
            data={
                "name": item_data['name'],
                "price": item_data['price']
            },
            files={
                "file": ("Itinerary.pdf", image_file, "application/pdf")
            }
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_delete(authorized_client, test_items):
    response = authorized_client.delete(f'/items/{test_items[0].id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_item_unauthorized(client):
    response = client.delete('/items/1')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_non_exist_item(authorized_client):
    response = authorized_client.delete('/items/800000')
    assert response.status_code == status.HTTP_404_NOT_FOUND