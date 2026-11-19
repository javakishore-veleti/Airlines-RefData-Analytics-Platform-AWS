#!/usr/bin/env bash
# Seed labels + epic/feature/story issues for milestones M0–M6.
# Safe to re-run for labels (--force). Issues are created fresh (do not re-run blindly).
set -euo pipefail

REPO="javakishore-veleti/Airlines-RefData-Analytics-Platform-AWS"

create_label() {
  local name="$1" color="$2"
  gh label create "$name" --repo "$REPO" --color "$color" --force >/dev/null
}

echo "Creating labels..."
create_label "type:epic" "6F42C1"
create_label "type:feature" "0052CC"
create_label "type:story" "0E8A16"
create_label "area:foundation" "BFD4F2"
create_label "area:cicd-local" "FBCA04"
create_label "area:cdc" "D93F0B"
create_label "area:middleware" "5319E7"
create_label "area:portal-admin" "1D76DB"
create_label "area:portal-intel" "006B75"
create_label "area:aws" "FF6900"

# milestone title → number
ms_num() {
  gh api "repos/${REPO}/milestones" --jq ".[] | select(.title==\"$1\") | .number"
}

M0=$(ms_num "M0 — Foundation & Superpowers")
M1=$(ms_num "M1 — Local platform bootstrap")
M2=$(ms_num "M2 — CDC to Iceberg (local)")
M3=$(ms_num "M3 — Middleware")
M4=$(ms_num "M4 — Airlines-RD-Admin")
M5=$(ms_num "M5 — Airlines-RD-Intelligence")
M6=$(ms_num "M6 — AWS cloud parity")

issue() {
  local title="$1" body="$2" milestone="$3"
  shift 3
  local labels=("$@")
  local args=(--repo "$REPO" --title "$title" --body "$body" --milestone "$milestone")
  local l
  for l in "${labels[@]}"; do
    args+=(--label "$l")
  done
  gh issue create "${args[@]}"
}

echo "Creating M0 issues..."
issue "[Epic] E0.1 Superpowers & agent contract" \
"## Epic
Install and enforce Superpowers methodology for this repo.

### Features
- F0.1.1 Vendor Superpowers
- F0.1.2 Product docs

Parent milestone: M0
See docs/ROADMAP.md" \
"$M0" "type:epic" "area:foundation"

issue "[Feature] F0.1.1 Vendor Superpowers" \
"## Feature
Vendored skills + Cursor plugin guidance.

### Stories
- S0.1.1.1 Vendored skills + VERSION + README
- S0.1.1.2 Cursor rule / AGENTS.md workflow contract
- S0.1.1.3 Document /add-plugin superpowers for hooks

Parent epic: E0.1" \
"$M0" "type:feature" "area:foundation"

issue "[Story] S0.1.1.1 Vendored skills + VERSION + README" \
"Ensure \`superpowers/\` contains skills, hooks metadata, VERSION, and README describing sequential workflow." \
"$M0" "type:story" "area:foundation"

issue "[Story] S0.1.1.2 Cursor rule / AGENTS.md workflow contract" \
"Agents must follow brainstorm→plan→TDD→review→finish, one milestone at a time." \
"$M0" "type:story" "area:foundation"

issue "[Story] S0.1.1.3 Document /add-plugin superpowers" \
"README/AGENTS document Cursor marketplace install for hooks." \
"$M0" "type:story" "area:foundation"

issue "[Feature] F0.1.2 Product docs" \
"## Feature
README + ROADMAP synced to GitHub.

### Stories
- S0.1.2.1 README Introduction / Objective / Architecture
- S0.1.2.2 ROADMAP synced to milestones/issues

Parent epic: E0.1" \
"$M0" "type:feature" "area:foundation"

issue "[Story] S0.1.2.1 README Introduction / Objective / Architecture" \
"Keep README aligned with local-first + portals + Superpowers (no United Airlines branding)." \
"$M0" "type:story" "area:foundation"

issue "[Story] S0.1.2.2 ROADMAP synced to milestones/issues" \
"docs/ROADMAP.md matches GitHub milestones and issue hierarchy." \
"$M0" "type:story" "area:foundation"

issue "[Epic] E0.2 Repository skeleton" \
"## Epic
Create target directory placeholders without implementing services yet.

### Features
- F0.2.1 Directory placeholders

Parent milestone: M0" \
"$M0" "type:epic" "area:foundation"

issue "[Feature] F0.2.1 Directory placeholders" \
"## Feature
Stub trees for CICD/Local, Middleware, Portals.

### Stories
- S0.2.1.1 CICD/Local scripts + Kafka compose path stubs
- S0.2.1.2 Middleware/API-Services + Middleware/DAGs
- S0.2.1.3 Portals/Airlines-RD-Admin + Airlines-RD-Intelligence

Parent epic: E0.2" \
"$M0" "type:feature" "area:foundation"

issue "[Story] S0.2.1.1 CICD/Local path stubs" \
"Add placeholders for docker-all-up.sh, all-down.sh, all-status.sh, Kafka/docker-compose.yaml (no live containers required yet)." \
"$M0" "type:story" "area:foundation"

issue "[Story] S0.2.1.2 Middleware path stubs" \
"Add Middleware/API-Services and Middleware/DAGs placeholders + README notes." \
"$M0" "type:story" "area:foundation"

issue "[Story] S0.2.1.3 Portals path stubs" \
"Add Portals/Airlines-RD-Admin and Portals/Airlines-RD-Intelligence placeholders." \
"$M0" "type:story" "area:foundation"

echo "Creating M1 issues..."
issue "[Epic] E1.1 Docker lifecycle scripts" \
"## Epic
One-command local stack control under CICD/Local.

Parent milestone: M1" \
"$M1" "type:epic" "area:cicd-local"

issue "[Feature] F1.1.1 Control scripts" \
"## Feature
docker-all-up / all-down / all-status

### Stories
- S1.1.1.1 docker-all-up.sh
- S1.1.1.2 all-down.sh
- S1.1.1.3 all-status.sh

Parent epic: E1.1" \
"$M1" "type:feature" "area:cicd-local"

issue "[Story] S1.1.1.1 docker-all-up.sh" \
"Bring up all local compose stacks in dependency order." \
"$M1" "type:story" "area:cicd-local"

issue "[Story] S1.1.1.2 all-down.sh" \
"Tear down all local stacks cleanly." \
"$M1" "type:story" "area:cicd-local"

issue "[Story] S1.1.1.3 all-status.sh" \
"Report health of MySQL, Kafka, Debezium, RabbitMQ, Airflow, object storage." \
"$M1" "type:story" "area:cicd-local"

issue "[Epic] E1.2 Compose services" \
"## Epic
MySQL, Kafka/Debezium, RabbitMQ, Airflow, MinIO via compose.

Parent milestone: M1" \
"$M1" "type:epic" "area:cicd-local"

issue "[Feature] F1.2.1 Data & messaging" \
"## Feature
MySQL + Kafka/Debezium + RabbitMQ

### Stories
- S1.2.1.1 MySQL binlog-ready + seed
- S1.2.1.2 CICD/Local/Kafka/docker-compose.yaml
- S1.2.1.3 RabbitMQ container

Parent epic: E1.2" \
"$M1" "type:feature" "area:cicd-local"

issue "[Story] S1.2.1.1 MySQL binlog-ready + seed" \
"Local MySQL with ROW binlog and market_db.market_rule seed data." \
"$M1" "type:story" "area:cicd-local"

issue "[Story] S1.2.1.2 Kafka docker-compose.yaml" \
"CICD/Local/Kafka/docker-compose.yaml with Kafka + Debezium Connect." \
"$M1" "type:story" "area:cicd-local"

issue "[Story] S1.2.1.3 RabbitMQ container" \
"RabbitMQ for API/portal async messaging." \
"$M1" "type:story" "area:cicd-local"

issue "[Feature] F1.2.2 Orchestration & storage" \
"## Feature
Airflow + MinIO + healthchecks

### Stories
- S1.2.2.1 Airflow with Middleware/DAGs mount
- S1.2.2.2 Local S3-compatible storage
- S1.2.2.3 Healthchecks wired to all-status.sh

Parent epic: E1.2" \
"$M1" "type:feature" "area:cicd-local"

issue "[Story] S1.2.2.1 Airflow + DAGs mount" \
"Airflow containers mount Middleware/DAGs as the DAG folder (relative path contract)." \
"$M1" "type:story" "area:cicd-local"

issue "[Story] S1.2.2.2 Local object storage" \
"MinIO (or equivalent) for Iceberg data/files." \
"$M1" "type:story" "area:cicd-local"

issue "[Story] S1.2.2.3 Healthchecks" \
"Each service has a probe used by all-status.sh." \
"$M1" "type:story" "area:cicd-local"

echo "Creating M2 issues..."
issue "[Epic] E2.1 Debezium CDC" \
"## Epic
Stream MySQL changes to Kafka via Debezium.

Parent milestone: M2" \
"$M2" "type:epic" "area:cdc"

issue "[Feature] F2.1.1 Connector" \
"## Feature
Debezium connector for market_rule

### Stories
- S2.1.1.1 Connector config
- S2.1.1.2 Topic naming + PK partition docs

Parent epic: E2.1" \
"$M2" "type:feature" "area:cdc"

issue "[Story] S2.1.1.1 Debezium connector for market_rule" \
"Connector captures market_db.market_rule insert/update/delete." \
"$M2" "type:story" "area:cdc"

issue "[Story] S2.1.1.2 Topic naming + PK partitioning" \
"Document topic names and partition-by-PK strategy." \
"$M2" "type:story" "area:cdc"

issue "[Epic] E2.2 Airflow batch apply" \
"## Epic
Batch Kafka CDC into Iceberg.

Parent milestone: M2" \
"$M2" "type:epic" "area:cdc"

issue "[Feature] F2.2.1 Kafka → Iceberg DAG" \
"## Feature
DAG under Middleware/DAGs

### Stories
- S2.2.1.1 Batch Kafka consumer DAG
- S2.2.1.2 Map c/u/d to Iceberg ops
- S2.2.1.3 Write + validate Iceberg tables

Parent epic: E2.2" \
"$M2" "type:feature" "area:cdc"

issue "[Story] S2.2.1.1 Batch Kafka consumer DAG" \
"Airflow DAG consumes Kafka CDC in configurable batches." \
"$M2" "type:story" "area:cdc"

issue "[Story] S2.2.1.2 Map Debezium ops to Iceberg" \
"Map c/u/d to insert/update/delete (merge semantics on rule_id)." \
"$M2" "type:story" "area:cdc"

issue "[Story] S2.2.1.3 Write + validate Iceberg" \
"Persist Iceberg on local object storage; validate with a local query path." \
"$M2" "type:story" "area:cdc"

echo "Creating M3 issues..."
issue "[Epic] E3.1 API Services" \
"## Epic
Middleware/API-Services for Admin + Intelligence.

Parent milestone: M3" \
"$M3" "type:epic" "area:middleware"

issue "[Feature] F3.1.1 Middleware/API-Services" \
"## Feature
API skeleton + RefData + Iceberg reads + RabbitMQ

### Stories
- S3.1.1.1 Service skeleton (health, config, OpenAPI)
- S3.1.1.2 RefData CRUD/publish vs MySQL
- S3.1.1.3 Iceberg/query façade for Intelligence
- S3.1.1.4 RabbitMQ integration

Parent epic: E3.1" \
"$M3" "type:feature" "area:middleware"

issue "[Story] S3.1.1.1 API service skeleton" \
"Health, config, OpenAPI for Middleware/API-Services." \
"$M3" "type:story" "area:middleware"

issue "[Story] S3.1.1.2 RefData CRUD/publish APIs" \
"Admin path APIs against MySQL reference data." \
"$M3" "type:story" "area:middleware"

issue "[Story] S3.1.1.3 Iceberg/query façade APIs" \
"Read APIs for Intelligence portal over lake data." \
"$M3" "type:story" "area:middleware"

issue "[Story] S3.1.1.4 RabbitMQ integration" \
"Async jobs/notifications via RabbitMQ." \
"$M3" "type:story" "area:middleware"

issue "[Epic] E3.2 DAG packaging" \
"## Epic
Stable Airflow-relative DAG layout and shared libs.

Parent milestone: M3" \
"$M3" "type:epic" "area:middleware"

issue "[Feature] F3.2.1 Airflow-relative DAGs" \
"## Feature
Mount contract + shared CDC/Iceberg libs

### Stories
- S3.2.1.1 Document relative mount path
- S3.2.1.2 Shared CDC parse + Iceberg writer libs

Parent epic: E3.2" \
"$M3" "type:feature" "area:middleware"

issue "[Story] S3.2.1.1 Document DAG mount path" \
"Document Middleware/DAGs relative path inside Airflow container." \
"$M3" "type:story" "area:middleware"

issue "[Story] S3.2.1.2 Shared CDC/Iceberg libs" \
"Reusable libraries for parse + Iceberg writes used by DAGs." \
"$M3" "type:story" "area:middleware"

echo "Creating M4 issues..."
issue "[Epic] E4.1 Admin portal" \
"## Epic
Portals/Airlines-RD-Admin for reference data management.

Parent milestone: M4" \
"$M4" "type:epic" "area:portal-admin"

issue "[Feature] F4.1.1 Airlines-RD-Admin" \
"## Feature
Admin UI wired to API-Services

### Stories
- S4.1.1.1 App shell + auth stub
- S4.1.1.2 Market rules CRUD/deactivate
- S4.1.1.3 CDC/pipeline status view
- S4.1.1.4 Wire to Middleware/API-Services

Parent epic: E4.1" \
"$M4" "type:feature" "area:portal-admin"

issue "[Story] S4.1.1.1 Admin app shell + auth stub" \
"Local app shell with auth stub for RD Admin." \
"$M4" "type:story" "area:portal-admin"

issue "[Story] S4.1.1.2 Market rules management UI" \
"List/create/update/deactivate market rules." \
"$M4" "type:story" "area:portal-admin"

issue "[Story] S4.1.1.3 CDC status view" \
"Show pipeline health summary for operators." \
"$M4" "type:story" "area:portal-admin"

issue "[Story] S4.1.1.4 Wire Admin to API-Services" \
"Integrate Admin portal with Middleware/API-Services." \
"$M4" "type:story" "area:portal-admin"

echo "Creating M5 issues..."
issue "[Epic] E5.1 Intelligence portal" \
"## Epic
Portals/Airlines-RD-Intelligence for analysts, risk managers, data managers.

Parent milestone: M5" \
"$M5" "type:epic" "area:portal-intel"

issue "[Feature] F5.1.1 Airlines-RD-Intelligence" \
"## Feature
View/query lake-backed reference data

### Stories
- S5.1.1.1 App shell + role-oriented nav
- S5.1.1.2 Browse/filter RefData
- S5.1.1.3 Ad-hoc query / saved views (scope TBD)
- S5.1.1.4 Wire to Middleware/API-Services

Parent epic: E5.1" \
"$M5" "type:feature" "area:portal-intel"

issue "[Story] S5.1.1.1 Intelligence app shell + roles" \
"Nav for analyst / risk / data manager personas." \
"$M5" "type:story" "area:portal-intel"

issue "[Story] S5.1.1.2 Browse/filter RefData" \
"Browse and filter Iceberg-backed reference data." \
"$M5" "type:story" "area:portal-intel"

issue "[Story] S5.1.1.3 Ad-hoc query / saved views" \
"Query UX scope finalized in Superpowers brainstorm for M5." \
"$M5" "type:story" "area:portal-intel"

issue "[Story] S5.1.1.4 Wire Intelligence to API-Services" \
"Integrate Intelligence portal with Middleware/API-Services." \
"$M5" "type:story" "area:portal-intel"

echo "Creating M6 issues..."
issue "[Epic] E6.1 AWS mapping" \
"## Epic
Map proven local pipeline to AWS. Do not start until explicit go-ahead.

Parent milestone: M6" \
"$M6" "type:epic" "area:aws"

issue "[Feature] F6.1.1 CloudFormation / IaC" \
"## Feature
AWS stack + cutover + ops

### Stories
- S6.1.1.1 Parameterized CloudFormation from blog sample
- S6.1.1.2 Local→AWS cutover runbook
- S6.1.1.3 Monitoring & cleanup procedures

Parent epic: E6.1" \
"$M6" "type:feature" "area:aws"

issue "[Story] S6.1.1.1 Parameterized CloudFormation" \
"Blog-aligned stack parameterized for this platform (no deploy until approved)." \
"$M6" "type:story" "area:aws"

issue "[Story] S6.1.1.2 Local→AWS cutover runbook" \
"Document mapping Debezium/Kafka/Airflow → DMS/Kinesis/Firehose." \
"$M6" "type:story" "area:aws"

issue "[Story] S6.1.1.3 Monitoring & cleanup" \
"CloudWatch/dashboard notes and cleanup order." \
"$M6" "type:story" "area:aws"

echo "Done. Open issues:"
gh issue list --repo "$REPO" --limit 100 --json number,title,milestone --jq '.[] | "\(.number)\t\(.milestone.title // "-")\t\(.title)"'
