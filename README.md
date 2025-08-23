# Quotes API Demo

A secure, multi-tenant **Quotes API** built with **FastAPI**. This is a demo project intended for portfolio use — showing how to design and secure a real-world style API.

## API Endpoints

| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| GET | `/v1/quotes` | List all quotes for tenant | viewer |
| POST | `/v1/quotes` | Create a new quote | manager |
| GET | `/v1/quotes/{quote_id}` | Get quote details | viewer |
| PUT | `/v1/quotes/{quote_id}` | Update quote status/customer | manager |
| DELETE | `/v1/quotes/{quote_id}` | Delete a quote | manager |

### Request/Response Examples

#### Create Quote
```json
POST /v1/quotes
{
    "customer": "Acme Corp",
    "items": [
        {
            "sku": "ITEM-1",
            "qty": 2,
            "unit_price": 99.50
        }
    ],
    "currency": "USD"
}
```

Response (201 Created):
```json
{
    "id": "quote-123",
    "customer": "Acme Corp",
    "items": [...],
    "currency": "USD",
    "created_at": "2025-08-23T10:00:00Z",
    "created_by": "user-123",
    "tenant_id": "tenant-1"
}
```

### Manual Testing
1. Generate a test token:
```bash
python ./scripts/make_jwt_token_hs256.py > token.txt
```

2. Set up environment:
```bash
export JWT=$(cat token.txt)
```

3. Test endpoints:
```bash
# List quotes
curl -H "Authorization: Bearer $JWT" http://localhost:8000/v1/quotes

# Create quote
curl -X POST http://localhost:8000/v1/quotes \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"customer":"Test Corp","items":[{"sku":"TEST-1","qty":1,"unit_price":100.00}],"currency":"USD"}'
```

## Features
- Authentication with **JWT** (audience, issuer, expiration validation)
- Role-based authorization (e.g., `viewer` vs `manager`)
- Multi-tenant data isolation
- Input validation with Pydantic models
- Postman collection for easy testing
- Optional FastAPI implementation for local testing


## Tech Stack
- **Python (FastAPI)** for REST API development
- **JWT** for authentication and authorization
- **pytest** for testing
- **GitHub Actions** for CI/CD

## Run Locally (FastAPI Edition)
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install development dependencies:
```bash
pip install pytest pytest-cov httpx
```

3. Start server:
```bash
uvicorn fastapi.app.main:app --reload
```

4. Visit API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
3. Generate and save a JWT token (with `scripts/make_jwt_hs256.py`):
```bash
python ./scripts/make_jwt_token_hs256.py > token.txt
JWT="$(cat token.txt)"
```
4. call endpoints:
```bash
curl -v -H "Authorization: Bearer $JWT" http://localhost:8000/v1/quotes
```

## Example Request
```bash
curl -X POST -H "Authorization: Bearer $JWT" -H "x-api-key: $API_KEY" -H "Content-Type: application/json" \
-d '{"customer":"Globex","items":[{"sku":"SKU-1","qty":2,"unit_price":99.5}],"currency":"USD"}' \
$BASE/v1/quotes
```