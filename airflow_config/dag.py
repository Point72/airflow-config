from inspect import currentframe
from typing import Any, cast
from uuid import uuid4

from airflow.models.dag import DAG as BaseDag

from .configuration.base import Configuration
from .utils import _get_calling_dag, _get_dag_root

__all__ = ("generate_dag_id", "create_dag", "DAG")


class DAG(BaseDag):
    def __init__(self, config: Configuration = None, **kwargs):
        if config:
            config.pre_apply(self, kwargs)
            print(kwargs)
        super().__init__(**kwargs)
        if config:
            config.apply(self)


def generate_dag_id(name: str = "", dag_root: str = "", *args: str, **kwargs: str) -> str:
    if not name:
        try:
            # get file of calling python file, can't use the module name as one might
            # have the same module in multiple folders
            caller = _get_calling_dag()

            # remove python suffix, replace path with dash
            name = caller.replace(".py", "").replace("/", "-").replace("_", "-")
            # remove root folder
            dag_root = dag_root or _get_dag_root()
            name = name.replace(dag_root.replace("/", "-").replace("_", "-"), "")
            while name.startswith("-"):
                name = name[1:]
        except Exception:
            name = cast(str, uuid4())
    return name


def create_dag(dag_id: str = "", config: Configuration = None, *args: Any, **kwargs: Any) -> DAG:
    dag = DAG(
        config=config,
        dag_id=dag_id or generate_dag_id(),
    )
    currentframe().f_back.f_back.f_globals[dag_id] = dag
    return dag