import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook

def audit_logs(dag_id,task_id,log_level,log_message) -> None:
    """

    """
    log_dict = [{
    "dag_id":dag_id,
    "task_id":task_id,
    "log_level":log_level,
    "message":log_message,
    }]
    postgres_hook_engine = PostgresHook(postgres_conn_id='opentax_postgres_conn').get_sqlalchemy_engine()
    log_df = pd.DataFrame(log_dict)

    log_df.to_sql('task_execution_logs', con=postgres_hook_engine,if_exists='append', index=False)
