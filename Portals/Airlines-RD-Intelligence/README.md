# Airlines-RD-Intelligence

Angular Intelligence portal (D5): PrimeNG Aura, Lucide, navy/ice/sky.

## End-to-end local wiring (#49)

```bash
cd Middleware/AccountService-API && ./app-startup.sh   # :8111
cd Middleware/MasterData-API && ./app-startup.sh       # :8110

cd Portals/Airlines-RD-Intelligence
npm install
npm start   # http://127.0.0.1:4201
```

| UI area | Backend |
|---|---|
| Sign in / sign up | AccountService-API `:8111` |
| Browse / filter | MasterData lake API `:8110/lake/market-rules` |
| Saved views | Local browser storage + browse query params |

Default login: `arfd-admin` / `arfd-admin`
