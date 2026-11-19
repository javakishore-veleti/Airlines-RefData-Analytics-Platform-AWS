# Middleware/AccountService-API

Auth + user CRUD FastAPI service (D3 layering). Default port `8111`.

## Default local user (seeded on first user API call)

| Username | Password | Role |
|---|---|---|
| `arfd-admin` | `arfd-admin` | admin |

Passwords are stored as PBKDF2-SHA256 hashes (never plaintext).

```bash
./app-startup.sh && ./app-status.sh
curl -s http://127.0.0.1:8111/users
```

## Auth API (Angular client contract)

Base URL local: `http://127.0.0.1:8111`

| Method | Path | Body | Success |
|---|---|---|---|
| POST | `/auth/signup` | `{ "username", "password", "display_name?" }` | `{ ok, token, username, role }` |
| POST | `/auth/signin` | `{ "username", "password" }` | `{ ok, token, username, role }` |
| POST | `/auth/signout` | `{ "token" }` | `{ ok, message }` |

Store `token` in portal session/localStorage; send on later Admin/Intelligence calls as needed (Bearer optional for Phase 1).
