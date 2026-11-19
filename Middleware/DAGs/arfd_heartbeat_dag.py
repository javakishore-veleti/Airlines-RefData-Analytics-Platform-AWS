"""No-op heartbeat DAG — proves Middleware/DAGs is on the Airflow DAG path."""
from datetime import datetime

try:
    from airflow import DAG
    from airflow.operators.empty import EmptyOperator
except ImportError:  # Airflow not installed in this process
    DAG = None  # type: ignore

if DAG is not None:
    with DAG(
        dag_id="arfd_heartbeat",
        start_date=datetime(2026, 1, 1),
        schedule=None,
        catchup=False,
        tags=["arfd"],
    ) as dag:
        EmptyOperator(task_id="ok")
