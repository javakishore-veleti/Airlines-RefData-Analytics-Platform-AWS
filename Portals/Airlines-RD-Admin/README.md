# Airlines-RD-Admin

Angular Admin portal (D5): PrimeNG Aura light, Lucide icons, navy/ice/sky tokens.

## End-to-end local wiring (#43)

```bash
# APIs
cd Middleware/AccountService-API && ./app-startup.sh   # :8111
cd Middleware/MasterData-API && ./app-startup.sh       # :8110

# UI
cd Portals/Airlines-RD-Admin
npm install
npm start   # http://127.0.0.1:4200 (proxy.conf.json available)
```

| UI area | Backend |
|---|---|
| Sign in / sign up / User Management | AccountService-API `:8111` |
| Market rules + CDC generate | MasterData-API `:8110` |
| Pipeline health | MasterData + Account `/health` + lake read |

## Default local login

| Username | Password |
|---|---|
| `arfd-admin` | `arfd-admin` |
