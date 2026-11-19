"""MasterData-API FastAPI entrypoint (D3 modular monolith)."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import admin_cdc, health, market_rules

app = FastAPI(title="ARFD MasterData-API", version="0.4.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health.router)
app.include_router(admin_cdc.router)
app.include_router(market_rules.router)


def create_app() -> FastAPI:
    return app
