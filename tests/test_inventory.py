def _product(client, on_hand=5):
    client.post("/api/v1/categories", json={"slug": "lenses", "name": "Lenses"})
    client.post(
        "/api/v1/products",
        json={
            "sku": "LENS-200",
            "name": "Clear Daily Lens",
            "price_cents": 149000,
            "category_slug": "lenses",
            "initial_on_hand": on_hand,
        },
    )


def test_atp_and_reserve(client):
    _product(client, on_hand=5)

    promise = client.get("/api/v1/inventory/LENS-200/atp", params={"quantity": 4})
    assert promise.status_code == 200
    assert promise.json()["can_fulfill"] is True

    reserved = client.post("/api/v1/inventory/LENS-200/reserve", json={"quantity": 4})
    assert reserved.status_code == 200
    assert reserved.json()["available"] == 1

    blocked = client.post("/api/v1/inventory/LENS-200/reserve", json={"quantity": 2})
    assert blocked.status_code == 409


def test_receive_increases_available_stock(client):
    _product(client, on_hand=1)
    response = client.post("/api/v1/inventory/LENS-200/receive", json={"quantity": 9})
    assert response.status_code == 200
    assert response.json()["available"] == 10
