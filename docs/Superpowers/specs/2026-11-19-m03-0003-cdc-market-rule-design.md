# M03-0003 — Configure CDC for `market_db.market_rule`

**Story:** #23  
**Date:** 2026-11-19  
**Status:** Approved (autonomous — operator requested decisions without further Q&A)

## Goal

Capture INSERT / UPDATE / DELETE on `market_db.market_rule` into the local streaming path so later M03 stories can apply to the lake.

## Decisions

1. **Connector:** Debezium MySQL connector on the existing `CICD/Local/Kafka` Connect cluster (`quay.io/debezium/connect:2.5`, port `8083`).
2. **Scope:** `table.include.list=market_db.market_rule` only (no other tables in this story).
3. **Identity:** `database.server.id=5400`, `topic.prefix=arfd` (topics look like `arfd.market_db.market_rule`). Final topic/key strategy is refined in story #24; this story uses Debezium defaults with that prefix.
4. **MySQL reachability from Connect:** JDBC URL host `host.docker.internal` and port from `ARFD_MYSQL_PORT` (default `3306`, local override often `3307`). User `arfd` with replication grants from M02 init SQL.
5. **Config in repo:** `CICD/Local/Kafka/connectors/market-rule-mysql.json` plus `register-market-rule-connector.sh` that PUTs/POSTs to Connect REST (`http://127.0.0.1:8083`).
6. **Verification:** After register, Connect reports `RUNNING`; a small INSERT/UPDATE/DELETE (or Admin CDC generate) produces messages on the `arfd.market_db.market_rule` topic (smoke via `kafka-console-consumer` or Connect API).
7. **Out of scope:** Iceberg apply (#26–#28), topic partitioning redesign (#24 beyond documenting the provisional prefix), AWS DMS.

## Acceptance mapping

| Acceptance | Delivery |
|---|---|
| Connector captures insert/update/delete for market_rule | Debezium MySQL connector + ROW binlog (already on ARFD MySQL) |
| Config checked into repo | JSON + register script under `CICD/Local/Kafka/` |

## Risks

- Separate Compose projects: Connect must use `host.docker.internal` (or a shared Docker network). Document in Local README.
- Port 3306 occupied by non-ARFD MySQL: operators set `ARFD_MYSQL_PORT=3307` in `.env` (D1 already shifts managed bind).
