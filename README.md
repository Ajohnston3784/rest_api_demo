# Quotes API Demo

A secure, multi-tenant **Quotes API** built with **FastAPI**. This is a demo project intended for portfolio use — showing how to design and secure a real-world style API.

See [AWS Deployment Guide](docs/aws_deployment.md) for instructions on deploying this API to AWS using Terraform and GitHub Actions.

## Features
- Authentication with **JWT** (audience, issuer, expiration validation)
- Role-based authorization (e.g., `viewer` vs `manager`)
- Multi-tenant data isolation
- Input validation with Pydantic models

## Tech Stack
- **Python (FastAPI)** for REST API development
- **JWT** for authentication and authorization
- **pytest** for testing
- **GitHub Actions** for CI/CD
- **Terraform** for infrastructure as code
- **AWS ECS Fargate** for container orchestration
- **AWS ECR** for container registry
- **AWS Application Load Balancer** for load balancing

## Getting Started

1. **Clone this repository**:
   ```bash
   git clone https://github.com/Ajohnston3784/rest_api_demo.git
   cd rest_api_demo
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your tenant**:
   Edit `scripts/make_jwt_token_hs256.py` and set your unique `tenant_id`:
   ```python
   "tenant_id": "your-name"  # Change this
   ```

4. **Generate JWT token**:
   ```bash
   python ./scripts/make_jwt_token_hs256.py > token.txt
   export JWT=$(cat token.txt)
   ```

5. **Start the server**:
   ```bash
   cd fastapi
   uvicorn app.main:app --reload
   ```

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| GET | `/v1/quotes` | List all quotes for tenant | viewer |
| POST | `/v1/quotes` | Create a new quote | manager |
| GET | `/v1/quotes/{quote_id}` | Get quote details | viewer |
| PUT | `/v1/quotes/{quote_id}` | Update quote status/customer | manager |
| DELETE | `/v1/quotes/{quote_id}` | Delete a quote | manager |

## Example Requests

### List Quotes (viewer role)
```bash
curl -H "Authorization: Bearer $JWT" http://localhost:8000/v1/quotes
```

### Create Quote (manager role)
```bash
curl -X POST http://localhost:8000/v1/quotes \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "Acme Corp",
    "items": [
        {
            "sku": "ITEM-1",
            "qty": 2,
            "unit_price": 99.50
        }
    ],
    "currency": "USD"
}'
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

## Important Notes
- Each user should use their own unique `tenant_id`
- JWT tokens include your tenant ID and roles (viewer/manager)
- Tokens expire after 24 hours - generate a new one if needed
- Keep your tenant ID simple (letters, numbers, hyphens only)
