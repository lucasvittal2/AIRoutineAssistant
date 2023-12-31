from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from Utils.strtime_handler import string_to_timedelta, string_to_datetime
from Utils.file_handler import read_yaml
from Env.paths import CONFIG_PATH, ETL_PATH

configs = read_yaml(CONFIG_PATH + 'app_config.yaml')
job_configs = configs['airflow']['todoist_job']
# Define the default arguments for the DAG
default_args = {
    'owner': job_configs['dag_owner'],
    'depends_on_past': False,
    'start_date': string_to_datetime(job_configs['dag_start_date']),
    'email': [job_configs['dag_email']],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries':job_configs['dag_retries'] ,
    'retry_delay': job_configs['dag_retry_delay'],
}

# Instantiate the DAG
dag = DAG(job_configs['dag_id'], default_args=default_args, schedule_interval=job_configs['schedule_interval'], catchup=False)

# Define the tasks



todoist_extract_data = BashOperator(
    task_id='todoist_extract_data',
    bash_command=f'python {ETL_PATH}/todoist/todoist_extract_data.py',
    retries=3,
    dag=dag,
)

load_todoist_data_on_stagging = BashOperator(
    task_id='load_todoist_data_on_stagging',
    bash_command=f'python {ETL_PATH}/todoist/load_todoist_data_on_stagging.py',
    retries=3,
    dag=dag,
)


load_todoist_data_to_dw = BashOperator(
    task_id='load_todoist_data_to_dw',
    bash_command=f'python {ETL_PATH}/todoist/load_todoist_data_to_dw.py',
    retries=3,
    dag=dag,
)

#Define the task dependencies
todoist_extract_data >> load_todoist_data_on_stagging >> load_todoist_data_to_dw