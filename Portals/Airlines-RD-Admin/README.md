# Airlines-RD-Admin

Angular Admin portal (D5): PrimeNG Aura light, Lucide icons, navy/ice/sky tokens.

## Local run

```bash
# Terminal A — AccountService (auth)
cd Middleware/AccountService-API && ./app-startup.sh

# Terminal B — Admin UI
cd Portals/Airlines-RD-Admin
npm install
npm start   # http://127.0.0.1:4200
```

## Default local login

| Username | Password |
|---|---|
| `arfd-admin` | `arfd-admin` |

Seeded by AccountService-API on first user/auth call.

## Layout

- Top bar + collapsible left nav + favicon
- Routes: Overview, Market rules, Pipeline health, **User Management**
- Signup / signin against AccountService-API (`ARFD_ACCOUNT_API` default `http://127.0.0.1:8111`)
