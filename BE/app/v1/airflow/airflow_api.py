from quart import Blueprint, request, jsonify
from .components.airflow_default import *


airflow_bp = Blueprint('airflow', __name__)

# DAG 실행
@airflow_bp.route('/dag/create', methods=['POST'])
async def create_dag():
    data = await request.json

    # DAG 생성 함수에서 요구하는 필수 입력 값 목록
    required_keys = ['user_id', 'dag_id', 'task_id', 'database_name', 'collection_name',
                     'filter_conditions', 'projection_fields', 'schedule_interval',
                     'output_format', 'output_destination']

    # 누락된 필수 입력 값 확인
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return jsonify({"error": f"다음 필수 입력 값이 누락되었습니다: {', '.join(missing_keys)}"}), 400

    # 입력 값 수집
    conf = {key: data[key] for key in required_keys}

    # DAG 실행 트리거
    response = await trigger_dag_run("create_dag", conf)
    if response.status_code == 200:
        return jsonify({"message": f"{conf['user_id']}의 DAG {conf['dag_id']} 생성이 요청되었습니다."}), 200
    else:
        return jsonify({"error": response.text}), response.status_code

# DAG 삭제
@airflow_bp.route('/dag/delete', methods=['POST'])
async def delete_dag():
    data = await request.json
    dag_id = data.get('dag_id')
    user_id = data.get('user_id')

    if not dag_id or not user_id:
        return jsonify({"error": "dag_id와 user_id는 필수 값입니다."}), 400

    conf = {
        "user_id": user_id,
        "dag_id": dag_id
    }

    response = await trigger_dag_run("delete_dag", conf)
    if response.status_code == 200:
        return jsonify({"message": f"DAG {dag_id} 삭제가 성공적으로 요청되었습니다."}), 200
    else:
        return jsonify({"error": response.text}), response.status_code

# DAG 목록 조회
@airflow_bp.route('/dag/list', methods=['POST'])
async def list_dags():
    data = await request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "user_id는 필수 값입니다."}), 400

    conf = {
        "user_id": user_id
    }

    response = await trigger_dag_run("list_dag", conf)
    if response.status_code == 200:
        return jsonify({"message": "DAG 목록 조회 성공"}), 200
    else:
        return jsonify({"error": response.text}), response.status_code

# DAG 상태 변경
@airflow_bp.route('/dag/status', methods=['PATCH'])
async def pause_dag():
    data = await request.json
    user_id = data.get('user_id')
    dag_id = data.get('dag_id')
    is_paused = data.get('is_paused')

    if not user_id or not dag_id:
        return jsonify({"error": "user_id와 dag_id는 필수 값입니다."}), 400

    if is_paused is None:
        return jsonify({"error": "is_paused는 필수 값입니다."}), 400

    # Airflow API 호출
    response = await change_dag_state(user_id, dag_id, is_paused)

    if response.status_code == 200:
        return jsonify({"message": "DAG 상태 변경 성공", "status": response.json()}), 200
    else:
        return jsonify({"error": response.text}), response.status_code