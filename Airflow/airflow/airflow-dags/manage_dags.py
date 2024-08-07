from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os

# DAGs를 저장할 디렉토리
DAG_DIR = "/opt/bitnami/airflow/dags"

# 기본 인자 설정
default_args = {
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

# 사용자별 새로운 DAG 생성 함수
def create_new_dag(**kwargs):
    if kwargs.get('execute_task') != 'create':  # execute_task가 'create'일 때만 실행
        return
    user_id = kwargs['user_id']
    dag_id = kwargs['dag_id']
    param1 = kwargs.get('param1', 'default1')
    param2 = kwargs.get('param2', 'default2')

    unique_dag_id = f"{user_id}_{dag_id}"
    dag_file_path = os.path.join(DAG_DIR, f"{unique_dag_id}.py")

    if os.path.exists(dag_file_path):
        print(f"DAG 파일 {dag_file_path}이 이미 존재합니다.")
        return

    dag_content = f"""
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {{
    'owner': '{user_id}',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}}

dag = DAG(
    '{unique_dag_id}',
    default_args=default_args,
    description='A dynamically generated DAG for {user_id}',
    schedule_interval='@daily',
    catchup=False,
    tags=['{user_id}']  # 사용자 ID를 태그로 추가해 접근 제한
)

def print_context(ds, **kwargs):
    print('Running task for user:', '{user_id}')
    print('Parameter 1:', '{param1}')
    print('Parameter 2:', '{param2}')
    return f'Logged date for {user_id}'

with dag:
    t1 = PythonOperator(
        task_id='print_date',
        python_callable=print_context,
    )
"""
    try:
        with open(dag_file_path, "w") as f:
            f.write(dag_content)
        print(f"Created DAG: {unique_dag_id}")
    except Exception as e:
        print(f"Error creating DAG: {e}")

# 사용자별 DAG 삭제 함수
def delete_dag(**kwargs):
    if kwargs.get('execute_task') != 'delete':  # execute_task가 'delete'일 때만 실행
        return
    user_id = kwargs['user_id']
    dag_id = kwargs['dag_id']

    unique_dag_id = f"{user_id}_{dag_id}"
    dag_file_path = os.path.join(DAG_DIR, f"{unique_dag_id}.py")

    if os.path.exists(dag_file_path):
        try:
            os.remove(dag_file_path)
            print(f"Deleted DAG: {unique_dag_id}")
        except Exception as e:
            print(f"Error deleting DAG: {e}")
    else:
        print(f"DAG file {dag_file_path} does not exist")

# 사용자별 DAG 목록 조회 함수
def list_dags(**kwargs):
    if kwargs.get('execute_task') != 'list':  # execute_task가 'list'일 때만 실행
        return
    user_id = kwargs['user_id']
    user_dags = [f for f in os.listdir(DAG_DIR) if f.startswith(f"{user_id}_") and f.endswith('.py')]
    print(f"{user_id}'s DAGs: {user_dags}")
    return user_dags

# DAG 정의 및 설정
with DAG('dag_manager', schedule_interval=None, default_args=default_args, access_control={'User': {'can_dag_read'}, 'Admin': {'can_dag_read', 'can_dag_edit'}}) as dag:

    # DAG 생성 Task
    create_dag_task = PythonOperator(
        task_id='create_new_dag',
        python_callable=create_new_dag,
        op_kwargs={
            'user_id': '{{ dag_run.conf["user_id"] }}',  # 사용자 ID
            'dag_id': '{{ dag_run.conf["dag_id"] }}',
            'execute_task': '{{ dag_run.conf["execute_task"] }}'  # 실행할 태스크 지정
        },
    )

    # DAG 삭제 Task
    delete_dag_task = PythonOperator(
        task_id='delete_dag',
        python_callable=delete_dag,
        op_kwargs={
            'user_id': '{{ dag_run.conf["user_id"] }}',  # 사용자 ID
            'dag_id': '{{ dag_run.conf["dag_id"] }}',
            'execute_task': '{{ dag_run.conf["execute_task"] }}'  # 실행할 태스크 지정
        },
    )

    # DAG 목록 조회 Task
    list_dags_task = PythonOperator(
        task_id='list_dags',
        python_callable=list_dags,
        op_kwargs={
            'user_id': '{{ dag_run.conf["user_id"] }}',  # 사용자 ID
            'execute_task': '{{ dag_run.conf["execute_task"] }}'  # 실행할 태스크 지정
        },
    )

    # 각 태스크는 독립적으로 실행될 수 있도록 의존성을 설정하지 않음

