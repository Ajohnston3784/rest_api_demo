from fastapi import Header
from .auth import decode_token, Claims

async def current_claims(authorization: str | None = Header(default=None)) -> Claims:
    """
    Dependency to get the current user's claims from the JWT token.
    """
    return decode_token(authorization) if authorization else Claims(sub="", tenant_id="", roles=[], scope=None)