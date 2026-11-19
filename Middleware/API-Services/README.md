# Middleware/API-Services

HTTP APIs for Airlines-RD-Admin (write path) and Airlines-RD-Intelligence (read/query path).

## M02 surface

Minimal FastAPI app for local bootstrap (D2):

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness + MySQL reachability |
| POST | `/admin/cdc/generate` | Body `{"count": N}` — INSERT/UPDATE `market_rule` to emit CDC |

```bash
cd Middleware/API-Services
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8100
```

Env: `ARFD_MYSQL_HOST`, `ARFD_MYSQL_PORT`, `ARFD_MYSQL_USER`, `ARFD_MYSQL_PASSWORD`, `ARFD_MYSQL_DATABASE` (defaults match `CICD/Local/.env.example`).

Full CRUD / Iceberg read APIs land in Milestone M04.
