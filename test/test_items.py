import pytest
from test.conftest import authorized_client, client, test_items
from fastapi import status
from app.schema import ItemOut


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


def test_create_item_invalid_data(authorized_client):
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


def test_update_item(authorized_client, test_items):
    item_data = {'name': 'cat', 'price': 20}
    with open('/Users/amanatanayak/Desktop/a.png', 'rb') as image_file:
        response = authorized_client.put(
            f'/items/{test_items[0].id}',
            data={
                "name": item_data['name'],
                "price": item_data['price']
            },
            files={
                "file": ("cat.jpeg", image_file, "image/jpeg")
            }
        )

    assert response.status_code == status.HTTP_200_OK


def test_unauthorized_update_item(client, test_items):
    item_data = {'name': 'cat', 'price': 20}
    with open('/Users/amanatanayak/Desktop/a.png', 'rb') as image_file:
        response = client.put(
            f'/items/{test_items[0].id}',
            data={
                "name": item_data['name'],
                "price": item_data['price']
            },
            files={
                "file": ("cat.jpeg", image_file, "image/jpeg")
            }
        )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_non_exist_item(authorized_client):
    item_data = {'name': 'cat', 'price': 20}
    with open('/Users/amanatanayak/Desktop/a.png', 'rb') as image_file:
        response = authorized_client.put(
            '/items/80000',
            data={
                "name": item_data['name'],
                "price": item_data['price']
            },
            files={
                "file": ("cat.jpeg", image_file, "image/jpeg")
            }
        )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_all_items(client, test_items):
    response = client.get('/items/')

    def validate(item):
        return ItemOut(**item)

    item_map = map(validate, response.json())
    item_list = list(item_map)

    assert len(response.json()) == len(item_list)
    assert response.status_code == status.HTTP_200_OK


def test_get_one_item(client, test_items):
    response = client.get(f'/items/{test_items[0].id}')
    item_data = ItemOut(**response.json())
    assert item_data.item.name == test_items[0].name
    assert item_data.item.price == test_items[0].price
    assert item_data.item.file_path == test_items[0].file_path


def test_get_one_non_exist_item(client):
    response = client.get('/items/78230')
    assert response.status_code == status.HTTP_404_NOT_FOUND
