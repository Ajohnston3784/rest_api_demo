from fastapi import FastAPI
from .routers import quotes

app = FastAPI(title="Quotes API", version="1.0.0")
app.include_router(quotes.router)