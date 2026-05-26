from uuid import uuid4


def auth_headers(client, return_user: bool = False):
    email = f"user-{uuid4().hex}@example.com"
    password = "StrongPassword123"

    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Test User",
        },
    )
    assert register_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    if return_user:
        return headers, {
            "email": email,
            "password": password,
            "full_name": "Test User",
        }

    return headers


def product_payload(**overrides):
    sku = f"LAP-{uuid4().hex[:8]}"
    payload = {
        "name": "Laptop",
        "sku": sku,
        "description": "Dell i7",
        "price": 50000,
        "stock_quantity": 10,
        "category": "Electronics",
    }
    payload.update(overrides)
    return payload


def create_product(client, headers, **overrides):
    response = client.post(
        "/products/",
        json=product_payload(**overrides),
        headers=headers,
    )
    assert response.status_code == 200
    return response.json()


def test_create_product(client):
    headers = auth_headers(client)
    response = client.post(
        "/products/",
        json=product_payload(),
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["owner"]["email"].startswith("user-")
    assert body["owner_id"] == body["owner"]["id"]


def test_get_current_user_profile(client):
    headers, user = auth_headers(client, return_user=True)

    response = client.get("/auth/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["email"] == user["email"]
    assert response.json()["full_name"] == user["full_name"]
    assert response.json()["role"] == "staff"


def test_get_current_user_profile_requires_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 403


def test_change_password(client):
    headers, user = auth_headers(client, return_user=True)
    new_password = "NewStrongPassword123"

    response = client.patch(
        "/auth/me/password",
        json={
            "current_password": user["password"],
            "new_password": new_password,
        },
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"

    old_login_response = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "password": user["password"],
        },
    )
    assert old_login_response.status_code == 401

    new_login_response = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "password": new_password,
        },
    )
    assert new_login_response.status_code == 200


def test_change_password_rejects_wrong_current_password(client):
    headers = auth_headers(client)

    response = client.patch(
        "/auth/me/password",
        json={
            "current_password": "wrong-password",
            "new_password": "NewStrongPassword123",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Current password is incorrect"


def test_get_products(client):
    headers = auth_headers(client)
    product = create_product(client, headers)

    response = client.get("/products/", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["id"] == product["id"]


def test_get_products_supports_pagination(client):
    headers = auth_headers(client)
    first = create_product(client, headers, name="First Laptop")
    second = create_product(client, headers, name="Second Laptop")

    first_page = client.get("/products/?limit=1", headers=headers)
    second_page = client.get("/products/?skip=1&limit=1", headers=headers)

    assert first_page.status_code == 200
    assert second_page.status_code == 200
    assert [product["id"] for product in first_page.json()] == [first["id"]]
    assert [product["id"] for product in second_page.json()] == [second["id"]]


def test_get_products_supports_search_and_category_filter(client):
    headers = auth_headers(client)
    matching = create_product(
        client,
        headers,
        name="Mechanical Keyboard",
        description="Backlit keys",
        category="Accessories",
    )
    create_product(client, headers, name="Office Chair", category="Furniture")

    response = client.get(
        "/products/?search=keyboard&category=Accessories",
        headers=headers,
    )

    assert response.status_code == 200
    assert [product["id"] for product in response.json()] == [matching["id"]]


def test_get_product(client):
    headers = auth_headers(client)
    product = create_product(client, headers)

    response = client.get(f"/products/{product['id']}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == product["id"]


def test_update_product(client):
    headers = auth_headers(client)
    product = create_product(client, headers)

    response = client.put(
        f"/products/{product['id']}",
        json={"price": 60000},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["price"] == 60000


def test_delete_product(client):
    headers = auth_headers(client)
    product = create_product(client, headers)

    response = client.delete(f"/products/{product['id']}", headers=headers)

    assert response.status_code == 200

    get_response = client.get(f"/products/{product['id']}", headers=headers)
    assert get_response.status_code == 404


def test_user_cannot_access_another_users_product(client):
    owner_headers = auth_headers(client)
    other_headers = auth_headers(client)
    product = create_product(client, owner_headers)

    response = client.get(f"/products/{product['id']}", headers=other_headers)

    assert response.status_code == 404
