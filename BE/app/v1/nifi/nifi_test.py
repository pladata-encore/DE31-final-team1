from quart import Blueprint, request, jsonify
from dotenv import load_dotenv
import os
import httpx

nifi_bp = Blueprint('nifi_test', __name__)
load_dotenv()

NIFI_URL = os.getenv("NIFI_URL") #https://192.168.1.234:8443/nifi-api/ 


# nifi가 접속이 되어있는 상태인가?
@nifi_bp.route('/access', methods=['GET', 'OPTIONS'])
async def get_nifi_access(): 
    url = f"{NIFI_URL}access/config"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight response'}), 200
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, headers=headers)
            print(f"Response Body: {response.text}")  
            return jsonify(response.json()), response.status_code
    except httpx.HTTPStatusError as e:
        return jsonify({"error": str(e)}), e.response.status_code
    except httpx.RequestError as e:
        return jsonify({"error": "Request error occurred"}), 500

# token 발행
@nifi_bp.route('/get_token', methods=['GET', 'OPTIONS'])
async def get_token():
    url = f"{NIFI_URL}access/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "username": "admin",
        "password": "admin_password"
    }
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight response'}), 200
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, headers=headers,data=data)
            print(f"Response Body: {response.text}")
            return response.text.strip()
    except httpx.HTTPStatusError as e:
        return jsonify({"error": str(e)}), e.response.status_code
    except httpx.RequestError as e:
        return jsonify({"error": "Request error occurred"}), 500

# 접속해있는 client_id 호출
@nifi_bp.route('/get_client_id', methods=['GET', 'OPTIONS'])
async def get_client_id():
    url = f"{NIFI_URL}flow/client-id"
    token = await get_token()
    if not token:
        return jsonify({"error": "Failed to retrieve token"}), 500
    headers = {"Authorization": f"Bearer {token}"}
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight response'}), 200
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, headers=headers)
            print(f"Response Body: {response.text}")  
            return response.text.strip()
    except httpx.HTTPStatusError as e:
        return jsonify({"error": str(e)}), e.response.status_code
    except httpx.RequestError as e:
        return jsonify({"error": "Request error occurred"}), 500


# user마다 고유의 user_process_group 생성 쉽게말해 작업폴더
@nifi_bp.route('/create_user_process_group', methods=['GET', 'OPTIONS'])
async def create_user_process_group():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight response'}), 200
    token = await get_token()
    client_id = await get_client_id()
    if not token:
        return jsonify({"error": "Failed to retrieve token"}), 500
    if not token:
        return jsonify({"error": "Failed to retrieve client_id"}), 500
    url = f"{NIFI_URL}process-groups/root/process-groups"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    body = {
        "revision": {
            "clientId": client_id,
            "version": 0,
            "lastModifier": "admin"
        },
        "component": {
            "name": "test",
            "position": {
                "x": 500.0,
                "y": 300.0
            }
        }
    }
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, headers=headers,json=body)
            # print(f"Response Body: {response.text}")  
            process_group_id = response.json().get("id")  # 'id' 필드 추출 # USER_PGID    
            return process_group_id
    except httpx.HTTPStatusError as e:
        return jsonify({"error": str(e)}), e.response.status_code
    except httpx.RequestError as e:
        return jsonify({"error": "Request error occurred"}), 500
  
 