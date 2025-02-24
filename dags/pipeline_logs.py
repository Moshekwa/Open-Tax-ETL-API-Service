import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook

def audit_logs(dag_id,task_id,log_level,log_message) -> None:
    """
    Logs task execution details into the `task_execution_logs` table in PostgreSQL.

    This function captures execution details of an Airflow DAG task, including the DAG ID,
    task ID, log level, and log message. The log is then stored in the PostgreSQL database.

    Args:
        dag_id (str): The unique identifier of the DAG.
        task_id (str): The unique identifier of the task within the DAG.
        log_level (str): The severity level of the log (e.g., 'INFO', 'ERROR', 'WARNING').
        log_message (str): The log message describing the event.

    Returns:
        None: The function writes the log to the database and does not return any value.

    Raises:
        SQLAlchemyError: If there is an issue with the database connection or execution.
        """
    try:
        log_dict = [{
        "dag_id":dag_id,
        "task_id":task_id,
        "log_level":log_level,
        "message":log_message,
        }]
        postgres_hook_engine = PostgresHook(postgres_conn_id='opentax_postgres_conn').get_sqlalchemy_engine()
        log_df = pd.DataFrame(log_dict)

        log_df.to_sql('task_execution_logs', con=postgres_hook_engine,if_exists='append', index=False)

    except SQLAlchemyError as e:
        raise RuntimeError(f"Failed to insert log into database: {str(e)}")