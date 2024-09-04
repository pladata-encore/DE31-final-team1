from quart import Blueprint
from .components.database import * 
from .components.authorization import *
from app.v1.nifi.components.nifi_default import *

main_dg = Blueprint('data_group',__name__)

# API LIST
# 1. get data group list (GET)
# 2. create data group (POST)
# 3. get data group info (GET)

@main_dg.route('/getdglist/', methods=['GET', 'OPTIONS'])
async def getlist():
    # check token
    status_message = await check_token(req.email, req.token)
    # split status message, first part is status code, else is message
    code, message = status_message.split('_', 1)

    # if code is "ERR" then return error message
    if code == "ERR":
        return message, 401

    # get data source list
    dg_list_data = get_dg_list(req.email)

    return dg_list_data, 200


@main_dg.route('/createdg/', methods=['POST', 'OPTIONS'])
async def createdg():
    # check token
    status_message = await check_token(req.email, req.token)
    # split status message, first part is status code, else is message
    code, message = status_message.split('_', 1)

    # if code is "ERR" then return error message
    if code == "ERR":
        return message, 401

    # create data group
    status_message = create_dg(req.email, req.dg_name, req.dg_desc, req.dg_data)
    # split status message, first part is status code, else is message
    code, message = status_message.split('_', 1)

    # if code is "ERR" then return error message
    if code == "ERR":
        return message, 400

    return message, 200
    
    

@main_dg.route('/getdginfo/', methods=['GET', 'OPTIONS'])
async def getinfo():
    # check token
    status_message = await check_token(req.email, req.token)
    # split status message, first part is status code, else is message
    code, message = status_message.split('_', 1)

    # if code is "ERR" then return error message
    if code == "ERR":
        return message, 401

    # get data group info and data
    dg_info = get_dg_info(req.email, req.dg_id)
    dg_data = get_dg_data(req.email, req.dg_id)

    dg_info_data = {
        "info": dg_info,
        "data": dg_data
    }

    return dg_info_data, 200

# user마다 고유의 user_process_group 생성 쉽게말해 작업폴더 http://localhost:19020/v1/users/createUser/
@nifi_default_bp.route('/create_user_process_group/', methods=['GET', 'OPTIONS'])
async def create_user_process_group(): # email로 중복체크를 하기에
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
            "name": "default",
            "position": {
                "x": 500.0,
                "y": 300.0
            }
        }
    }
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, headers=headers,json=body)
            print(f"Response Body: {response.text}")  
            process_group_id = response.json().get("id")  # 'id' 필드 추출 # USER_PGID    
        
            return process_group_id 
    except httpx.HTTPStatusError as e:
        return jsonify({"error": str(e)}), e.response.status_code
    except httpx.RequestError as e:
        return jsonify({"error": "Request error occurred"}), 500


# userid의 pgid 가져오기 
@nifi_default_bp.route('/get_processor_group_id/', methods=['GET', 'OPTIONS'])
async def get_processor_group_id(): # email로 중복체크를 하기에
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight response'}), 200
    

   
    
    
    
  
 