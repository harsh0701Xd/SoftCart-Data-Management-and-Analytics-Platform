from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import re
import os

# Define functions for tasks
def extract_data():
    with open("/home/project/airflow/dags/capstone/accesslog.txt", "r") as infile:
        data = infile.read()
        ip_addresses = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', data)
        with open("/home/project/airflow/dags/capstone/extracted_data.txt", "w") as outfile:
            for ip_address in ip_addresses:
                outfile.write(ip_address + '\n')

def transform_data():
    with open("/home/project/airflow/dags/capstone/extracted_data.txt", "r") as infile:
        transformed_lines = [line for line in infile if line.strip() != "198.46.149.143\n"]
        with open("/home/project/airflow/dags/capstone/transformed_data.txt", "w") as outfile:
            outfile.writelines(transformed_lines)

def load_data():
    os.system("tar -cvf /home/project/airflow/dags/capstone/weblog.tar /home/project/airflow/dags/capstone/transformed_data.txt")

# Define default arguments for the DAG
default_args = {
  'owner': 'airflow',
  'start_date': days_ago(0),
  'email': ['airflow@example.com'],
  'email_on_failure': True,
  'email_on_retry': True,
  'retries': 1,
  'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
  dag_id='process_web_log',
  schedule_interval=timedelta(days=1),
  default_args=default_args,
  description='A DAG to process web server log files daily',
  )


# Define tasks using PythonOperator
extract_data_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_data_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

# Define task dependencies
extract_data_task >> transform_data_task >> load_data_task
