from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd

def extract_transactional_data(**kwargs):
    #csv_file_path = 'data/financial_transactions.csv'
    csv_file_path = 'dags/data/financial_transactions.csv'
    df = pd.read_csv(csv_file_path)

    # Convert DataFrame to dictionary
    transaction_data_dict = df.to_dict(orient='records')  # 'records' creates a list of dictionaries
    kwargs['ti'].xcom_push(key='extracted_data', value=transaction_data_dict)

with DAG(
    dag_id="open_tax_etl",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@once",
    catchup=False
) as dag:
    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_transactional_data,
        provide_context=True,
    )

    extract_task