from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from datetime import datetime, timedelta
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

# from src.pydantic.url_model import validate_and_store
import sys
import os
# Calculate the absolute path to the src directory
# Add the src directory to sys.path

from src.pydantic_project.url_model import validate_and_store

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def branch_function(**kwargs):
    """Decides whether to run the webscraping task based on the trigger source."""
    trigger_source = kwargs.get('dag_run').conf.get('trigger_source', '')
    if trigger_source == 'streamlit':
        return 'run_scrapy_playwright'
    else:
        return 'skip_webscraping'

def upload_file_to_s3(bucket_name, s3_key, file_path):
    hook = S3Hook(aws_conn_id='aws_default')
    hook.load_file(filename=file_path, bucket_name=bucket_name, replace=True, key=s3_key)    


sql_file_path = '/opt/airflow/src/DBT-Snowflake.sql'

with open(sql_file_path, 'r') as file:
    sql_commands = file.read()

copy_into_table_sql = """
COPY INTO your_snowflake_table
FROM 's3://airflow-cfa/CFA.csv'
CREDENTIALS=(aws_key_id='YOUR_AWS_ACCESS_KEY_ID' aws_secret_key='YOUR_AWS_SECRET_ACCESS_KEY')
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);
"""

with DAG(
    'consolidated_dag',
    default_args=default_args,
    description='A consolidated dag for ETL',
    schedule=None,
    start_date=datetime(2024, 3, 25),
    catchup=False,
) as dag:

    decide_to_scrape = BranchPythonOperator(
        task_id='decide_to_scrape',
        python_callable=branch_function,
    )

    run_scrapy_playwright = BashOperator(
        task_id='run_scrapy_playwright',
        bash_command='cd /opt/airflow/src/scrapy/Pwspider/spiders && scrapy crawl pwspidey -o /opt/airflow/src/dataset/CFA.json',
    )
    skip_webscraping = EmptyOperator(
        task_id='skip_webscraping',
    )

    validate_and_store_task = PythonOperator(
        task_id='validate_and_store',
        python_callable=validate_and_store,
        op_kwargs={'json_file_path': '/opt/airflow/src/dataset/CFA.json', 'csv_file_path': '/opt/airflow/src/dataset/validated_CFA.csv'},
    )

    join_task= EmptyOperator(
        task_id='join_task',
        trigger_rule=TriggerRule.ONE_SUCCESS,
    )

    upload_to_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_file_to_s3,
        op_kwargs={'bucket_name': 'airflow-cfa', 's3_key': 'CFA.csv', 'file_path': '/opt/airflow/src/dataset/validated_CFA.csv'},
    )

    snowflake_upload = SnowflakeOperator(
    task_id='execute_sql_in_snowflake',
    snowflake_conn_id='snowflake_default',
    sql=sql_commands,
    dag=dag,
    )

    run_dbt_models = BashOperator(
    task_id='run_dbt_models',
    bash_command='dbt run --profiles-dir /opt/airflow/src/dbt_proj/ --project-dir /opt/airflow/src/dbt_proj/',
    )
    




    decide_to_scrape >> [run_scrapy_playwright, skip_webscraping] >> join_task >> validate_and_store_task >> upload_to_s3 >> snowflake_upload >> run_dbt_models