from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import DagModel
from datetime import timedelta
import os

# 기본 인자 설정
default_args = {
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

# 사용자 DAG를 삭제하는 Python 함수
def delete_user_dag(**kwargs):
    user_id = kwargs['dag_run'].conf.get('user_id')
    dag_id = kwargs['dag_run'].conf.get('dag_id')

    # 고유한 DAG ID를 설정
    unique_dag_id = f"{user_id}_{dag_id}"

    # DAG 디렉토리에서 파일을 삭제
    DAG_DIR = '/opt/bitnami/airflow/dags'
    dag_file_path = os.path.join(DAG_DIR, f"{unique_dag_id}.py")

    # DAG 파일이 있는지 확인하고 삭제
    if os.path.exists(dag_file_path):
        os.remove(dag_file_path)
        print(f"Deleted DAG file: {dag_file_path}")
    else:
        print(f"DAG 파일 {dag_file_path}이 존재하지 않습니다.")

# DAG 정의 및 설정
with DAG('delete_dag', schedule_interval=None, default_args=default_args) as dag:

    # PythonOperator를 사용하여 DAG 삭제 Task
    delete_dag_task = PythonOperator(
        task_id='delete_user_dag_task',
        python_callable=delete_user_dag,
        provide_context=True,
    )

