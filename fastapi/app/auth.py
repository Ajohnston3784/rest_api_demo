import os, jwt
from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import List

JWT_AUD = os.getenv("JWT_AUD", "quotes-api")
JWT_ISS = os.getenv("JWT_ISS", "https://auth.example.com")
JWT_SECRET = os.getenv("JWT_SECRET", "test-demo-secret")

class Claims(BaseModel):
    sub: str
    tenant_id: str
    roles: List[str] = []
    scope: str | None = None

def decode_token(bearer: str) -> Claims:
    # Validate that the token is provided and follows the 'Bearer <token>' format.
    if not bearer or not bearer.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid token",
        )
    # Extract the JWT from the header.
    token = bearer.split(" ", 1)[1]
    try:
        # Decode the JWT using the secret and validate its audience and issuer.
        p = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], audience=JWT_AUD, issuer=JWT_ISS)
        return Claims(sub=p.get("sub", ""), tenant_id=p.get("tenant_id", ""), roles=p.get("roles", []), scope=p.get("scope"))
    except Exception:
        # If decoding fails, raise an HTTP unauthorized error.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
def require_role(claims: Claims, role: str):
    if role not in claims.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role '{role}' is required",
        )