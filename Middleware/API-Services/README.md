# Middleware/API-Services

HTTP APIs for Airlines-RD-Admin (write path) and Airlines-RD-Intelligence (read/query path).

## M02 surface

Minimal FastAPI app for local bootstrap (D2):

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness + MySQL reachability |
| POST | `/admin/cdc/generate` | Body `{"count": N}` — mixed INSERT/UPDATE/DELETE on `market_rule` for CDC |

```bash
cd Middleware/API-Services
pip install -r requirements.txt
./run.sh   # ARFD_API_PORT default 8110
# or: uvicorn app.main:app --host 127.0.0.1 --port 8110
```

Env: `ARFD_MYSQL_*`, `ARFD_API_HOST`, `ARFD_API_PORT` (defaults match `CICD/Local/.env.example`).

Full CRUD / Iceberg read APIs land in Milestone M04.
