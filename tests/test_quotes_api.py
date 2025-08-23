import time
import jwt
from fastapi.testclient import TestClient
from app.main import app

SECRET = "test-demo-secret"
ISS = "https://auth.example.com"
AUD = "quotes-api"

# Test data fixtures
TEST_QUOTE_SIMPLE = {
    "customer": "Test Customer",
    "items": [
        {
            "sku": "TEST-1",
            "qty": 1,
            "unit_price": 100.00
        }
    ],
    "currency": "USD"
}

TEST_QUOTE_COMPLEX = {
    "customer": "Complex Customer",
    "items": [
        {
            "sku": "ITEM-1",
            "qty": 2,
            "unit_price": 50.00
        },
        {
            "sku": "ITEM-2",
            "qty": 1,
            "unit_price": 150.00
        }
    ],
    "currency": "EUR"
}

def make_token(roles=("viewer",), tenant_id="acme-co", secret=SECRET):
    return jwt.encode({
        "sub": "test-user",
        "tenant_id": tenant_id,
        "roles": roles,
        "iss": ISS,
        "aud": AUD,
        "exp": int(time.time()) + 3600,  # Token valid for 1 hour
    }, secret, algorithm="HS256")

client= TestClient(app)

def test_list_quotes():
    response = client.get(
        "/v1/quotes",
        headers={"Authorization": f"Bearer {make_token()}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_quote():
    response = client.post(
        "/v1/quotes",
        json=TEST_QUOTE_SIMPLE,
        headers={"Authorization": f"Bearer {make_token(roles=['manager'])}"}
    )

    assert response.status_code == 201
    assert response.json()["customer"] == "Test Customer"
    assert response.json()["currency"] == "USD"


def test_create_complex_quote():
    response = client.post(
        "/v1/quotes",
        json=TEST_QUOTE_COMPLEX,
        headers={"Authorization": f"Bearer {make_token(roles=['manager'])}"}
    )

    assert response.status_code == 201
    assert response.json()["customer"] == "Complex Customer"
    assert response.json()["currency"] == "EUR"
    assert len(response.json()["items"]) == 2

def test_get_quote():
    create_response = client.post(
        "/v1/quotes",
        json=TEST_QUOTE_SIMPLE,
        headers={"Authorization": f"Bearer {make_token(roles=['manager'])}"}
    )
    
    quote_id = create_response.json()["id"]
    
    response = client.get(
        f"/v1/quotes/{quote_id}",
        headers={"Authorization": f"Bearer {make_token()}"}
    )
    
    assert response.status_code == 200
    assert response.json()["id"] == quote_id

def test_delete_quote():
    create_response = client.post(
        "/v1/quotes",
        json=TEST_QUOTE_SIMPLE,
        headers={"Authorization": f"Bearer {make_token(roles=['manager'])}"}
    )
    
    quote_id = create_response.json()["id"]
    
    response = client.delete(
        f"/v1/quotes/{quote_id}",
        headers={"Authorization": f"Bearer {make_token(roles=['manager'])}"}
    )
    
    assert response.status_code == 204

def test_update_quote():
    create_response = client.post(
        "/v1/quotes",
        json=TEST_QUOTE_SIMPLE,
        headers={"Authorization": f"Bearer {make_token(roles=['manager'])}"}
    )
    
    quote_id = create_response.json()["id"]
    
    response = client.put(
        f"/v1/quotes/{quote_id}?status=approved&customer=Updated+Customer",
        headers={"Authorization": f"Bearer {make_token(roles=['manager'])}"}
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
    assert response.json()["customer"] == "Updated Customer"

def test_list_requires_auth():
    response = client.get(
        f"/v1/quotes",
        headers={"Authorization": f"Bearer {make_token(secret='wrong-secret')}"}
    )
     
    assert response.status_code == 401

def test_create_requires_manager():
    response = client.post(
        "/v1/quotes",
        json=TEST_QUOTE_SIMPLE,
        headers={"Authorization": f"Bearer {make_token(roles=['sales'])}"}
    )
    print(response.json())

    assert response.status_code == 403