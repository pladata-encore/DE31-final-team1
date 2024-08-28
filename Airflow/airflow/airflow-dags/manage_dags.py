from airflow import DAG
fom airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
import os

# DAGs를 저장할 디렉토리
DAG_DIR = "/opt/bitnami/airflow/dags"

# 기본 인자 설정
default_args = {
    'start_date': days_ago(1),
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
    catchup=False,
    tags=['{user_id}']  # 사용자 ID를 태그로 추가해 접근 제한
)

def print_context(ds, **kwargs):
    print('Running task for user:', '{user_id}')
    print('Parameter 1:', '{param1}')
    print('Parameter 2:', '{param2}')
    return f'Logged date for {user_id}'

with dag:
    t1 = KubernetesPodOperator(
        namespace='airflow',
        image="python:3.8-slim",
        cmds=["python", "-c"],
        arguments=["print_context(ds='{{ ds }}', **{{ task_instance.xcom_pull(task_ids='print_date') }})"],
        name="airflow-task-pod",
        task_id='print_date',
        get_logs=True,
        is_delete_operator_pod=True
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
    create_dag_task = KubernetesPodOperator(
        task_id='create_new_dag',
        namespace='airflow',
        image='python:3.8-slim',
        cmds=['python', '-c'],
        arguments=[
            "from manage_dag import create_new_dag; create_new_dag(user_id='{{ dag_run.conf['user_id'] }}', dag_id='{{ dag_run.conf['dag_id'] }}', execute_task='{{ dag_run.conf['execute_task'] }}')"
        ],
        name='create-dag-task-pod',
        get_logs=True,
        is_delete_operator_pod=True,
    )

    # DAG 삭제 Task
    delete_dag_task = KubernetesPodOperator(
        task_id='delete_dag',
        namespace='airflow',
        image='python:3.8-slim',
        cmds=['python', '-c'],
        arguments=[
            "from manage_dag import delete_dag; delete_dag(user_id='{{ dag_run.conf['user_id'] }}', dag_id='{{ dag_run.conf['dag_id'] }}', execute_task='{{ dag_run.conf['execute_task'] }}')"
        ],
        name='delete-dag-task-pod',
        get_logs=True,
        is_delete_operator_pod=True,
    )

    # DAG 목록 조회 Task
    list_dags_task = KubernetesPodOperator(
        task_id='list_dags',
        namespace='airflow',
        image='python:3.8-slim',
        cmds=['python', '-c'],
        arguments=[
            "from manage_dag import list_dags; list_dags(user_id='{{ dag_run.conf['user_id'] }}', execute_task='{{ dag_run.conf['execute_task'] }}')"
        ],
        name='list-dags-task-pod',
        get_logs=True,
        is_delete_operator_pod=True,
    )

    # 각 태스크는 독립적으로 실행될 수 있도록 의존성을 설정하지 않음
