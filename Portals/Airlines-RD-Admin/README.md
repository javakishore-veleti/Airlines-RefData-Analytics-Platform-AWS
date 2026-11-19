# Airlines-RD-Admin

Reference Data Admin portal — manage source reference data and trigger CDC simulation.

## M02

Open `index.html` (or serve the directory) for **Generate CDC events**. It POSTs to Middleware `POST /admin/cdc/generate`.

```bash
# API must be running (see Middleware/MasterData-API/README.md)
python -m http.server 5500 --directory Portals/Airlines-RD-Admin
# open http://127.0.0.1:5500/
```

Full portal shell / CRUD lands in Milestone M05.
