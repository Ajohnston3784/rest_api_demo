from typing import List
from pydantic import BaseModel

class QuoteItem(BaseModel):
    sku: str
    qty: int
    unit_price: float

class QuoteCreate(BaseModel):
    customer: str
    items: List[QuoteItem]
    currency: str = 'USD'

class QuoteOut(BaseModel):
    id: str
    tenant_id: str
    customer: str
    items: List[QuoteItem]
    currency: str
    status: str
    created_at: int
    created_by: str
    total: float

