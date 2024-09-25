from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import os
import json
from jinja2 import Template

# 기본 인자 설정
default_args = {
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

# 새로운 DAG 파일을 생성하는 Python 함수
def create_new_dag(**kwargs):
    # dag_run.conf에서 모든 사용자 입력 값 가져오기
    conf = kwargs['dag_run'].conf

    required_keys = ['user_id', 'dag_id', 'task_id', 'database_name', 'collection_name',
                     'filter_conditions', 'projection_fields', 'schedule_interval',
                     'output_format', 'output_destination']

    # 필수 입력 값이 모두 있는지 확인
    for key in required_keys:
        if key not in conf:
            raise ValueError(f"필수 입력 값 '{key}'가 제공되지 않았습니다.")

    user_id = conf.get('user_id')
    dag_id = conf.get('dag_id')
    task_id = conf.get('task_id')
    database_name = conf.get('database_name')
    collection_name = conf.get('collection_name')
    filter_conditions = conf.get('filter_conditions')
    projection_fields = conf.get('projection_fields')
    schedule_interval = conf.get('schedule_interval')
    output_format = conf.get('output_format')
    output_destination = conf.get('output_destination')

    # 입력 값 검증 (JSON 형식 확인)
    try:
        filter_conditions_json = json.loads(filter_conditions)
    except json.JSONDecodeError:
        raise ValueError("filter_conditions가 유효한 JSON 형식이 아닙니다.")

    try:
        if isinstance(projection_fields, str):
            projection_fields_list = json.loads(projection_fields)
        elif isinstance(projection_fields, list):
            projection_fields_list = projection_fields
        else:
            raise ValueError
    except:
        raise ValueError("projection_fields가 유효한 리스트 형식의 JSON이 아닙니다.")

    # DAG 파일 생성 경로 설정
    DAG_DIR = '/opt/bitnami/airflow/dags'
    unique_dag_id = f"{user_id}_{dag_id}"
    dag_file_path = os.path.join(DAG_DIR, f"{unique_dag_id}.py")

    # DAG 템플릿 정의
    dag_template = Template('''
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from pymongo import MongoClient
import json
import csv

# 기본 인자 설정
default_args = {
    'owner': '{{ user_id }}',
    'start_date': days_ago(1),
    'retries': 1,
}

# DAG 정의
with DAG(
    dag_id='{{ unique_dag_id }}',
    default_args=default_args,
    description='Extract data from MongoDB and save as {{ output_format }}',
    schedule_interval={{ schedule_interval }},
    catchup=False,
) as dag:

    def extract_data_from_mongo(**context):
        from airflow.providers.mongo.hooks.mongo import MongoHook

        # MongoDB 연결
        hook = MongoHook(conn_id='mongo_default')
        db = hook.get_conn()['{{ database_name }}']
        collection = db['{{ collection_name }}']

        # 필터 조건 및 프로젝션 적용
        filter_conditions = {{ filter_conditions }}
        projection_fields = { field: 1 for field in {{ projection_fields }} }

        # 데이터 추출
        data = collection.find(filter_conditions, projection_fields)

        # 데이터 저장
        output_format = '{{ output_format }}'
        output_destination = '{{ output_destination }}'

        data_list = list(data)
        if output_format.lower() == 'json':
            with open(output_destination, 'w') as f:
                json.dump(data_list, f, default=str)
        elif output_format.lower() == 'csv':
            if data_list:
                keys = data_list[0].keys()
                with open(output_destination, 'w', newline='') as f:
                    dict_writer = csv.DictWriter(f, keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(data_list)
        else:
            raise ValueError('지원되지 않는 출력 형식입니다.')

    extract_task = PythonOperator(
        task_id='{{ task_id }}',
        python_callable=extract_data_from_mongo,
        provide_context=True,
    )
''')

    # schedule_interval 처리
    if schedule_interval.lower() == 'none':
        schedule_interval_value = None
    else:
        schedule_interval_value = f"'{schedule_interval}'"

    # 템플릿 렌더링
    dag_content = dag_template.render(
        user_id=user_id,
        unique_dag_id=unique_dag_id,
        task_id=task_id,
        database_name=database_name,
        collection_name=collection_name,
        filter_conditions=json.dumps(filter_conditions_json),
        projection_fields=json.dumps(projection_fields_list),
        output_format=output_format,
        output_destination=output_destination,
        schedule_interval=schedule_interval_value
    )

    # DAG 파일 생성 (존재하지 않을 경우에만 생성)
    if not os.path.exists(dag_file_path):
        with open(dag_file_path, 'w') as f:
            f.write(dag_content)
        print(f"DAG 파일이 생성되었습니다: {dag_file_path}")
    else:
        print(f"DAG 파일 {dag_file_path}이 이미 존재합니다.")

# create_dag DAG 정의 및 설정
with DAG('create_dag', schedule_interval=None, default_args=default_args, catchup=False) as dag:

    create_dag_task = PythonOperator(
        task_id='create_new_dag',
        python_callable=create_new_dag,
        provide_context=True,
    )
