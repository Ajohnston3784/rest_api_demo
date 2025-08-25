# Quotes API Demo

A secure, multi-tenant **Quotes API** built with **FastAPI**. This is a demo project intended for portfolio use — showing how to design and secure a real-world style API.

See [AWS Deployment Guide](docs/aws_deployment.md) for instructions on deploying this API to AWS using Terraform and GitHub Actions.

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
- Optional FastAPI implementation for local testing


## Tech Stack
- **Python (FastAPI)** for REST API development
- **JWT** for authentication and authorization
- **pytest** for testing
- **GitHub Actions** for CI/CD
- **Terraform** for infrastructure as code
- **AWS ECS Fargate** for container orchestration
- **AWS ECR** for container registry
- **AWS Application Load Balancer** for load balancing

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

## Accessing the API

This API can be accessed in two ways:

1. **Local Development**: 
   - URL: `http://localhost:8000`
   - Use the instructions above in "Run Locally"

2. **AWS Deployment**:

The API is deployed and available for testing at:
```bash
export API_URL=<your-actual-alb-dns-name>  # Replace with your actual ALB DNS
```

To access the API:

1. **Clone this repository**:
   ```bash
   git clone https://github.com/Ajohnston3784/rest_api_demo.git
   cd rest_api_demo
   ```

2. **Install Python dependencies** (needed for token generation):
   ```bash
   pip install python-jose
   ```

3. **Generate your JWT token**:
   ```bash
   # Edit the tenant_id in scripts/make_jwt_token_hs256.py
   # Change this line:
   #   "tenant_id": "tenant-1"
   # to your unique tenant ID, e.g.:
   #   "tenant_id": "your-name"

   python ./scripts/make_jwt_token_hs256.py > token.txt
   export JWT=$(cat token.txt)
   ```

4. **Test the API**:
   ```bash
   # List quotes (viewer role)
   curl -H "Authorization: Bearer $JWT" http://$API_URL/v1/quotes

   # Create a quote (manager role)
   curl -X POST http://$API_URL/v1/quotes \
     -H "Authorization: Bearer $JWT" \
     -H "Content-Type: application/json" \
     -d '{"customer":"Test Corp","items":[{"sku":"TEST-1","qty":1,"unit_price":100.00}],"currency":"USD"}'
   ```

5. **View API Documentation**:
   - Swagger UI: `http://$API_URL/docs`
   - ReDoc: `http://$API_URL/redoc`

**Important Notes**:
- It's recommended that each user uses their own unique `tenant_id` (can be anything)
- The JWT token includes your tenant ID and roles (viewer/manager)
- Tokens expire after 24 hours - generate a new one if needed
- Keep your tenant ID simple (letters, numbers, hyphens only)
