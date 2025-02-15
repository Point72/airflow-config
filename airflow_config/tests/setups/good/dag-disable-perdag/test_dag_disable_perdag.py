from unittest.mock import patch

from airflow_config import DAG, load_config


def test_create_dag_from_config():
    with patch("sys.exit") as sys_exit:
        conf = load_config("config", "test")
        DAG(dag_id="testdag", config=conf)
        assert sys_exit.call_count == 1
        DAG(dag_id="example_dag", config=conf)
        assert sys_exit.call_count == 1
        DAG(dag_id="example_da2", config=conf)
        assert sys_exit.call_count == 2
