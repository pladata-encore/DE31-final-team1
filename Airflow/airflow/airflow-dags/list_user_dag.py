from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import DagBag
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=3)
}

# 특정 사용자가 소유한 DAG 목록을 출력하는 함수
def list_user_dags(**kwargs):
    # DAG 실행 시 전달된 conf 값에서 user_id 가져오기
    user_id = kwargs['dag_run'].conf.get('user_id', None)

    if not user_id:
        print("user_id가 제공되지 않았습니다.")
        return

    # DagBag을 통해 모든 DAG 가져오기
    dag_bag = DagBag()
    # user_id를 포함하는 DAG 목록 필터링
    user_dags = [dag_id for dag_id in dag_bag.dags if dag_id.startswith(f"{user_id}_")]

    if user_dags:
        print(f"사용자 {user_id}의 DAG 목록: {user_dags}")
    else:
        print(f"사용자 {user_id}에 해당하는 DAG가 없습니다.")
    return user_dags

# DAG 정의 및 설정
with DAG(
    dag_id='list_dag',    
    default_args=default_args,
    schedule_interval=None,  # 수동 트리거
    catchup=False,
) as dag:

    list_dags_task = PythonOperator(
        task_id='list_user_dags_task',
        python_callable=list_user_dags,
        provide_context=True,  # context에서 dag_run을 가져오기 위해 필요
    )

