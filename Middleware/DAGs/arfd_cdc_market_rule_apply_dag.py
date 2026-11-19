"""Airflow DAG: batch-apply market_rule CDC to the local lake (story #26)."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator

REPO = Path(__file__).resolve().parents[2]
APPLY = REPO / "scripts" / "cdc_apply_market_rule.py"
VERIFY = REPO / "scripts" / "verify_lake_market_rule.py"
LAKE = REPO / "runtime_data" / "lake"

default_args = {
    "owner": "arfd",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="arfd_cdc_market_rule_apply",
    description="Consume arfd.market_db.market_rule and write lake files",
    default_args=default_args,
    start_date=datetime(2026, 11, 19),
    schedule_interval="*/10 * * * *",
    catchup=False,
    tags=["arfd", "cdc", "lake"],
) as dag:
    apply = BashOperator(
        task_id="apply_cdc_batch",
        bash_command=(
            f"ARFD_LAKE_ROOT={LAKE} ARFD_KAFKA_BOOTSTRAP=${{ARFD_KAFKA_BOOTSTRAP:-127.0.0.1:9092}} "
            f"python3 {APPLY} --max-messages 500 --timeout-sec 30"
        ),
    )
    verify = BashOperator(
        task_id="verify_lake_rows",
        bash_command=f"ARFD_LAKE_ROOT={LAKE} python3 {VERIFY} --min-rows 1",
    )
    apply >> verify
