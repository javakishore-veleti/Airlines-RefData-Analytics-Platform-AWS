"""MasterData-API FastAPI entrypoint (D3 modular monolith)."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import admin_cdc, health, lake_query, market_rules, messaging

app = FastAPI(title="ARFD MasterData-API", version="0.6.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health.router)
app.include_router(admin_cdc.router)
app.include_router(market_rules.router)
app.include_router(lake_query.router)
app.include_router(messaging.router)


def create_app() -> FastAPI:
    return app
