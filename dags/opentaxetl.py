import logging
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd
from pipeline_logs import audit_logs

# Configure logging format to include timestamps for audit
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def extract_transactional_data(**kwargs):
    try:
        #csv_file_path = 'data/financial_transactions.csv'
        logging.info('Beginning to extract data from source')
        csv_file_path = 'dags/data/financial_transactions.csv'
        df = pd.read_csv(csv_file_path)

        # Convert DataFrame to dictionary
        transaction_data_dict = df.to_dict(orient='records')  # 'records' creates a list of dictionaries
        #transaction_data_dict = df.to_json()
        kwargs['ti'].xcom_push(key='extracted_data', value=transaction_data_dict)

        dag_id = kwargs['dag'].dag_id
        task_id = kwargs['task'].task_id

        #engine = PostgresHook(postgres_conn_id='opentax_postgres_conn').get_sqlalchemy_engine()
        audit_logs(dag_id,task_id,'INFO','Succesfully Extracted Data from CSV')
        logging.info('Data Extraction Completed')
    except Exception as e:
        dag_id = kwargs['dag'].dag_id
        task_id = kwargs['task'].task_id

        audit_logs(dag_id,task_id,'ERROR',str(e))
        logging.error('Failed to extract Data from CSV')

def transform_data(**kwargs):
    """
    Transform the input DataFrame by cleaning and processing the data in the following order:
    1. Remove dollar sign from the 'amount' column and convert to float
    2. Fill NaN values in the 'amount' column with 0
    3. Convert 'transaction_date' to datetime encforcing errors
    4. Drop duplicate rows, keeping rows with the same tranasction_id from different users

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing transaction data.

    Returns:
        pd.DataFrame: The transformed DataFrame.
    """
    try:

        logging.info('Beginning Data Processing')

        task_instance = kwargs['ti']
        extracted_data = task_instance.xcom_pull(task_ids='extract_task', key='extracted_data')

        dataframe = pd.DataFrame(extracted_data)

        dataframe['amount'] = dataframe['amount'].fillna(0)
        dataframe['amount'] = dataframe['amount'].str.replace('$', '', regex=False).astype(float)

        dataframe['transaction_date'] = pd.to_datetime(dataframe['transaction_date'], errors='coerce', dayfirst=True)
        dataframe['transaction_date'] = dataframe['transaction_date'].dt.strftime('%Y-%m-%d')

        # Replacing unknown date records with an invalid date
        dataframe['transaction_date'] = dataframe['transaction_date'].fillna('1970-01-01')

        dataframe.drop_duplicates(inplace=True)
        transformed_data_dict = dataframe.to_dict(orient='records')

        kwargs['ti'].xcom_push(key='transformed_data', value=transformed_data_dict)

        dag_id = kwargs['dag'].dag_id
        task_id = kwargs['task'].task_id

        # engine = PostgresHook(postgres_conn_id='opentax_postgres_conn').get_sqlalchemy_engine()
        audit_logs(dag_id, task_id, 'INFO', f'Succesfully Processed and Transformed {len(dataframe)} rows')
        logging.info('Data Processing Completed')

    except Exception as e:
        dag_id = kwargs['dag'].dag_id
        task_id = kwargs['task'].task_id

        audit_logs(dag_id, task_id, 'ERROR', str(e))
        logging.error(f'Failed to transform data: str{e}')

def load_transactional_data(**kwargs):
    """

    """
    try:
        logging.info('Executing data loading into target table')
        ti = kwargs['ti']
        transformed_data = ti.xcom_pull(task_ids='transform_task', key='transformed_data')

        df = pd.DataFrame(transformed_data)

        postgres_hook = PostgresHook(postgres_conn_id='opentax_postgres_conn')

        # Get SQLAlchemy engine from the hook
        engine = postgres_hook.get_sqlalchemy_engine()

        # Insert DataFrame into PostgreSQL
        df.to_sql('transactions', con=engine, if_exists='replace', index=True)

        dag_id = kwargs['dag'].dag_id
        task_id = kwargs['task'].task_id
        audit_logs(dag_id, task_id, 'INFO', f'Succesfully Loaded {len(df)} rows to the Open Tax Database')
        logging.info('Data loading into target table completed')

    except Exception as e:
        dag_id = kwargs['dag'].dag_id
        task_id = kwargs['task'].task_id

        audit_logs(dag_id, task_id, 'ERROR', str(e))
        logging.error(f'Failed to load data: str{e}')

with DAG(
    dag_id="open_tax_etl",
    description='A simple OpenTax ETL pipeline using Airflow',
    start_date=datetime(2023, 1, 1),
    schedule_interval="@once", # Triggers DAG Execution at Midnight
    catchup=False
) as dag:
    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_transactional_data,
        provide_context=True,
    )
    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_data,
        provide_context=True
    )
    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load_transactional_data,
        provide_context=True
    )

    extract_task >> transform_task >> load_task
