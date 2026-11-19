from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health, users
app = FastAPI(title="ARFD AccountService-API", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(health.router)
app.include_router(users.router)
def create_app() -> FastAPI:
    return app
