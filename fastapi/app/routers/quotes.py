from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import current_claims
from ..schemas import QuoteOut, QuoteCreate
from ..db import db
from ..auth import require_role, Claims

router = APIRouter(prefix="/v1/quotes", tags=["quotes"])

@router.get("/", response_model=list[QuoteOut])
def list_quotes(claims: Claims = Depends(current_claims)):
    return db.list(claims.tenant_id)

@router.post("/", response_model=QuoteOut, status_code=201)
def create_quote(payload: QuoteCreate, claims: Claims = Depends(current_claims)):
    require_role(claims, "manager")
    return db.create(claims.tenant_id, payload.customer, [i.model_dump() for i in payload.items], payload.currency, claims.sub)

@router.get("/{quote_id}", response_model=QuoteOut)
def get_quote(quote_id: str, claims: Claims = Depends(current_claims)):
    quote = db.get(claims.tenant_id, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote

@router.put("/{quote_id}", response_model=QuoteOut)
def update_quote(quote_id: str, status: str, customer: str, claims: Claims = Depends(current_claims)):
    require_role(claims, "manager")
    quote = db.update(claims.tenant_id, quote_id, status=status, customer=customer)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote

@router.delete("/{quote_id}", status_code=204)
def delete_quote(quote_id: str, claims: Claims = Depends(current_claims)):
    require_role(claims, "manager")
    db.delete(claims.tenant_id, quote_id)