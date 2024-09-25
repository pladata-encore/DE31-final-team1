from quart import Blueprint, request, jsonify
from .components.airflow_default import trigger_dag_run

airflow_bp = Blueprint('airflow', __name__)

# DAG 실행
@airflow_bp.route('/dag/create', methods=['POST'])
async def create_dag():
    data = await request.json
    dag_id = data.get('dag_id')
    user_id = data.get('user_id')

    if not dag_id or not user_id:
        return jsonify({"error": "dag_id와 user_id는 필수 값입니다."}), 400

    conf = {
        "user_id": user_id,
        "dag_id": dag_id
    }

    response = await trigger_dag_run("create_dag", conf)
    if response.status_code == 200:
        return jsonify({"message": f"DAG {user_id}의 {dag_id} 생성이 요청되었습니다."}), 200
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
