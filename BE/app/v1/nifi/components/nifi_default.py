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
            print(f"Response Body: {response.text}")
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
            print(f"Response Body: {response.text}")  
            return response.text.strip()
    except httpx.HTTPStatusError as e:
        return jsonify({"error": str(e)}), e.response.status_code
    except httpx.RequestError as e:
        return jsonify({"error": "Request error occurred"}), 500