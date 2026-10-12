def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_list_product(client):
    created = client.post("/api/v1/categories", json={"slug": "frames", "name": "Frames"})
    assert created.status_code == 201

    product = client.post(
        "/api/v1/products",
        json={
            "sku": "FRAME-100",
            "name": "Harbor Round Frame",
            "description": "Acetate round frame.",
            "price_cents": 890000,
            "currency": "inr",
            "category_slug": "frames",
            "initial_on_hand": 12,
        },
    )
    assert product.status_code == 201
    body = product.json()
    assert body["currency"] == "INR"
    assert body["available"] == 12

    listing = client.get("/api/v1/products", params={"q": "round", "category": "frames"})
    assert listing.status_code == 200
    assert listing.json()["total"] == 1


def test_duplicate_sku_is_rejected(client):
    client.post("/api/v1/categories", json={"slug": "frames", "name": "Frames"})
    payload = {
        "sku": "FRAME-100",
        "name": "Harbor Round Frame",
        "price_cents": 100,
        "category_slug": "frames",
    }
    assert client.post("/api/v1/products", json=payload).status_code == 201
    conflict = client.post("/api/v1/products", json=payload)
    assert conflict.status_code == 409


def test_unknown_product_returns_404(client):
    response = client.get("/api/v1/products/MISSING")
    assert response.status_code == 404
