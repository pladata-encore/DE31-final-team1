from quart import Blueprint, request, jsonify
from app.v1.subprocess.components.common import check_token
from .components.subprocess_manager import subprocess_manager

subprocess_bp = Blueprint('subprocess', __name__)

@subprocess_bp.route('/start-collection/', methods=['POST', 'OPTIONS'])
async def start_collection():

    req = await request.get_json()
    email = req.get("email")
    ds_id = req.get("ds_id")
    token = req.get("access_token")

    token_status = await check_token(email, token)
    if token_status.startswith("ERR"):
        return jsonify({"error": token_status}), 400

    if subprocess_manager.start_process(email, ds_id):
        return jsonify({"message": "Data collection started"}), 200
    
    else:
        return jsonify({"error": "Process already running"}), 400


@subprocess_bp.route('/stop-collection/', methods=['POST', 'OPTIONS'])
async def stop_collection():
    req = await request.get_json()
    email = req.get("email")
    token = req.get("access_token")

    token_status = await check_token(email, token)
    if token_status.startswith("ERR"):
        return jsonify({"error": token_status}), 400

    if subprocess_manager.stop_process(email):
        return jsonify({"message": "Data collection stopped"}), 200
    
    else:
        return jsonify({"error": "No running process found"}), 400