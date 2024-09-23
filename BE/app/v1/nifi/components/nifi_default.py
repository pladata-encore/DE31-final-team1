from app.v1.subprocess.components.common import check_token
from quart import Blueprint, request, jsonify
from dotenv import load_dotenv
from quart import jsonify, Response  

import os
import httpx
from app.v1.users.components.common import *
import aiohttp

nifi_default_bp = Blueprint('nifi_default', __name__)
load_dotenv()

NIFI_URL = os.getenv("NIFI_URL") #https://192.168.1.234:8443/nifi-api/ 

# nifi가 접속이 되어있는 상태인가? http://localhost:19020/v1/nifi_default/access/
@nifi_default_bp.route('/access/', methods=['GET', 'OPTIONS'])
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




# token 발행 http://localhost:19020/v1/nifi_default/get_token/
@nifi_default_bp.route('/get_token/', methods=['GET', 'OPTIONS'])
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
            # print(f"Response Body: {response.text}")
            return response.text.strip()
    except httpx.HTTPStatusError as e:
        return jsonify({"error": str(e)}), e.response.status_code
    except httpx.RequestError as e:
        return jsonify({"error": "Request error occurred"}), 500

# 접속해있는 client_id 호출 http://localhost:19020/v1/nifi_default/get_client_id/
@nifi_default_bp.route('/get_client_id/', methods=['GET', 'OPTIONS'])
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
            # print(f"Response Body: {response.text}")  
            return response.text.strip()
    except httpx.HTTPStatusError as e:
        return jsonify({"error": str(e)}), e.response.status_code
    except httpx.RequestError as e:
        return jsonify({"error": "Request error occurred"}), 500

# 생성되어있는 default process group 삭제 http://localhost:19020/v1/nifi_default/delete_all_pg/
@nifi_default_bp.route('/delete_all_pg/', methods=['GET', 'OPTIONS'])
async def delete_all_pg():
    url = f"{NIFI_URL}process-groups/root/process-groups"
    token = await get_token()
    if not token:
        return jsonify({"error": "Failed to retrieve token"}), 500
    headers = {"Authorization": f"Bearer {token}"}
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight response'}), 200
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, headers=headers)
            # print(f"Response Body: {response.text}")  
            response_data = json.loads(response.text)
            process_groups = response_data.get('processGroups', [])
            for process_group in process_groups:
                process_group_id = process_group.get('id')
                process_group_name = process_group.get('component').get('name')
                process_group_version = process_group.get('revision').get('version')
                # print(f"Process Group ID: {process_group.get('id')}, name: {process_group.get('component').get('name')}")
                client_id = await get_client_id()
                delete_url = f"{NIFI_URL}process-groups/{process_group_id}?version={process_group_version}&clientId={client_id}"
                delete_response = await client.delete(delete_url, headers=headers)
                if delete_response.status_code == 200:
                    print(f"Successfully deleted Process Group ID: {process_group_id}, Name: {process_group_name}")
                else:
                    print(f"Failed to delete Process Group ID: {process_group_id}, Name: {process_group_name}")
                    return jsonify({"error": f"Failed to delete process group {process_group_name}"}), delete_response.status_code

            return jsonify({"message": "All process groups deleted successfully"}), 200
    except httpx.HTTPStatusError as e:
        return jsonify({"error": str(e)}), e.response.status_code
    except httpx.RequestError as e:
        return jsonify({"error": "Request error occurred"}), 500

# UserID로 user_process_group_id 가져오기  http://localhost:19020/v1/nifi_default/get_user_process_group_id/
@nifi_default_bp.route('/get_user_process_group_id/', methods=['GET', 'OPTIONS'])
async def get_user_process_group_id():
    # 현재 접속한 휍 email 과 token 값 가져오기
    req = await request.get_json()
    email = req.get("email")
    token = req.get("access_token")

    token_status = await check_token(email, token)

    # db token과 web token 값이 다르다
    if token_status.startswith("ERR"):
        return jsonify({"error": token_status}), 400
    
    else:
        async with get_session() as session:
            search = await session.execute(select(UserPGInfo.PgID).where(UserPGInfo.UserEmail == req.email))
            pg_id = search.scalar()
            return pg_id, 200

   