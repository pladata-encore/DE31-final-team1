from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import os

# 기본 인자 설정
default_args = {
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

# 새로운 DAG 파일을 생성하는 Python 함수
def create_new_dag(**kwargs):
    user_id = kwargs['dag_run'].conf.get('user_id')
    dag_id = kwargs['dag_run'].conf.get('dag_id')

    DAG_DIR = '/opt/bitnami/airflow/dags'
    unique_dag_id = f"{user_id}_{dag_id}"
    dag_file_path = os.path.join(DAG_DIR, f"{unique_dag_id}.py")

    dag_content = f"""
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

default_args = {{
    'owner': '{user_id}',
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}}

dag = DAG(
    '{unique_dag_id}',
    default_args=default_args,
    description='A dynamically generated DAG for {user_id}',
    schedule_interval='@daily',
    catchup=False
)

with dag:
    run_pod_task = KubernetesPodOperator(
        namespace='airflow',
        image='python:3.8-slim',
        cmds=['python', '-c'],
        arguments=["from datetime import datetime\\nprint('Today is ' + str(datetime.now()))"],
        labels={{"task": "pod_task"}},
        name='run-pod-task',
        task_id='run_pod_task',
        get_logs=True,
        is_delete_operator_pod=True,
    )
"""

    if not os.path.exists(dag_file_path):
        with open(dag_file_path, 'w') as f:
            f.write(dag_content)
        print(f"Created DAG: {unique_dag_id}")
    else:
        print(f"DAG 파일 {dag_file_path}이 이미 존재합니다.")

# DAG 정의 및 설정
with DAG('create_dag', schedule_interval=None, default_args=default_args) as dag:

    # PythonOperator를 사용하여 DAG 생성 Task
    create_dag_task = PythonOperator(
        task_id='create_new_dag',
        python_callable=create_new_dag,
        provide_context=True,
    )
