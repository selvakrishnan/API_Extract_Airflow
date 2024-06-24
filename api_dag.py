import json
from datetime import datetime
from airflow.models import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

def save_posts(ti) -> None:
    posts=ti.xcom_pull(task_ids=['get_posts'])
    with open('path_to_save_the_data','w') as f: #provide your path
        json.dump(posts[0],f)

with DAG(
    dag_id='api_dag',
    schedule_interval=None,
    start_date=days_ago(2))as dag:

    api_active=HttpSensor(
    task_id='api_website',
    http_conn_id='api_posts',
    endpoint='posts/')
    
    task_to_retrive = SimpleHttpOperator(
    task_id='get_posts',
    http_conn_id='api_posts',
    endpoint='posts/',
    method='GET',
    response_filter=lambda response: json.loads(response.text),
    log_response=True)
    
    task_save=PythonOperator(
    task_id='save_posts',
    python_callable=save_posts)

    api_active >> task_to_retrive >> task_save
