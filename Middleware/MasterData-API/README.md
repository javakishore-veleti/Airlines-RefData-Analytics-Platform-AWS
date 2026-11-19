# Middleware/MasterData-API

FastAPI modular monolith for Airlines reference-data writes and lake reads (D3).

## Layers

`api → facade → WF → tasks → dao` with Ctx/Req/Resp DTOs and per-layer `object_factory.py`.

## Endpoints (M04 skeleton)

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness + MySQL via layered Health use case |
| POST | `/admin/cdc/generate` | GenerateCdcEvents via full D3 layering |
| POST | `/admin/market-rules` | Create market rule |
| PUT | `/admin/market-rules/{id}` | Update market rule |
| POST | `/admin/market-rules/{id}/deactivate` | Deactivate market rule |
| GET | `/docs` | OpenAPI |

```bash
cd Middleware/MasterData-API
pip install -r requirements.txt
./app-startup.sh
./app-status.sh
./app-shutdown.sh
# foreground: ./run.sh
```

Env: `ARFD_MYSQL_*`, `ARFD_API_HOST`, `ARFD_API_PORT` (defaults match `CICD/Local/.env.example`).

```bash
python3 -m unittest discover -s tests -v
```
