import sqlite3
import os
import time
import uuid
import json
from typing import List

DB_PATH = os.getenv("DB_PATH", ":memory:")
SCHEMA = """
CREATE TABLE IF NOT EXISTS quotes (
    id TEXT PRIMARY KEY,
    tenant_id TEXT,
    customer TEXT,
    items TEXT,
    currency TEXT,
    status TEXT,
    created_at INTEGER,
    created_by TEXT,
    total REAL
);
CREATE INDEX IF NOT EXISTS idx_tenant_id ON quotes (tenant_id);
"""

class DB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        for stmt in SCHEMA.strip().split(";"):
            stmt = stmt.strip()
            if stmt:
                self.conn.execute(stmt)
        self.conn.commit()

    def list(self, tenant_id: str):
        rows = self.conn.execute("SELECT * FROM quotes WHERE tenant_id = ? ORDER BY created_at DESC", (tenant_id,)).fetchall()
        return [self._d(r) for r in rows]
    
    def get(self, tenant_id: str, quote_id: str):
        row = self.conn.execute("SELECT * FROM quotes WHERE tenant_id = ? AND id = ?", (tenant_id, quote_id)).fetchone()
        if row:
            return self._d(row)
        return None
    
    def create(self, tenant_id: str, customer: str, items: List, currency: str, created_by: str):
        quote_id = f"q_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        total = sum(item['qty'] * item['unit_price'] for item in items)
        created_at = int(time.time())
        self.conn.execute(
            "INSERT INTO quotes (id, tenant_id, customer, items, currency, status, created_at, created_by, total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (quote_id, tenant_id, customer, json.dumps(items), currency, "draft", created_at, created_by, total)
        )
        self.conn.commit()
        return self.get(tenant_id, quote_id)
    
    def update(self, tenant_id: str, quote_id: str, status: str = None, customer: str = None):
        if status is not None: 
            self.conn.execute("UPDATE quotes SET status = ? WHERE tenant_id = ? AND id = ?", (status, tenant_id, quote_id))
        if customer is not None: 
            self.conn.execute("UPDATE quotes SET customer = ? WHERE tenant_id = ? AND id = ?", (customer, tenant_id, quote_id))
        self.conn.commit()
        return self.get(tenant_id, quote_id)
    
    def delete(self, tenant_id: str, quote_id: str):
        self.conn.execute("DELETE FROM quotes WHERE tenant_id = ? AND id = ?", (tenant_id, quote_id))
        self.conn.commit()

    @staticmethod
    def _d(r):
        if not r: return None
        return {"id": r[0], "tenant_id": r[1], "customer": r[2], "items": json.loads(r[3]), 
                "currency": r[4], "status": r[5], "created_at": r[6], "created_by": r[7], "total": r[8]}
    
db = DB()