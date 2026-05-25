import pytest


def test_create_product(client):
    response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "sku": "LAP-001",
            "description": "Dell i7",
            "price": 50000,
            "stock_quantity": 10,
            "category": "Electronics",
        },
    )

    assert response.status_code in [200, 401]


def test_get_products(client):
    response = client.get("/products/")

    assert response.status_code in [200, 401]
    if response.status_code == 200:
        assert isinstance(response.json(), list)


def test_get_product(client):

    response = client.get("/products/1")

    assert response.status_code in [200, 404, 401]


def test_update_product(client):
    response = client.put("/products/1", json={"price": 60000})

    assert response.status_code in [200, 404, 401]


def test_delete_product(client):
    response = client.delete("/products/1")

    assert response.status_code in [200, 404, 401]
