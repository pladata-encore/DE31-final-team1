from quart import Blueprint
from .components.common import *
from .components.functions import *
from app.v1.nifi.nifi_api import *
from app.v1.nifi.components.nifi_default import *

main_bp = Blueprint('main',__name__)

@main_bp.route('/createUser/', methods=['POST', 'OPTIONS'])
async def createUser():

        pr = await preflight_request()
        if(pr):
            return pr

        
        # 정합성 체크
        success, req = await json_validation(require_name=True)

        if not success:
            return req
        
        # 유저 생성
        success, created, status_code = await create_user(req.email, req.name, req.pwd)
        print(success, created, status_code)
        if not success:
            return created, status_code
        
        return created, status_code
    

@main_bp.route('/login/', methods=['POST', 'OPTIONS'])
async def login():

        pr = await preflight_request()
        if(pr):
            return pr
        
        # 정합성 체크
        success, req = await json_validation(require_name=False)

        if not success:
            return req
        
        # 로그인
        success, login_token, status_code = await login_validation(req.email, req.pwd)

        if not success:
              return login_token, status_code
        
        return login_token, status_code
        
@main_bp.route('/rule_set_default/',methods=['GET','OPTIONS'])
async def rule_set_default():
    # test용으로 152번째 userid -> pgid -> processor id -> 추가적으로 connection까지

    # 152번째 user의 pgid 가져오기
    UserId = 152
    user_process_group_id = await get_user_process_group_id(UserId)
    print(user_process_group_id)
    # processor_list에 관한 정보 받기 , id, name, properties, type, version만
    user_processor_list = await get_processors_list(UserId)
    # ids = [processor['ID'] for processor in user_processor_list]

    # connection 목록
    user_connection_list = await get_all_connection(UserId)

    
    result_dict = {
        "processors": user_processor_list,
        "connections": user_connection_list
    }

    # print(ids)
    return jsonify(result_dict)

# consemkafka 수정하기
@main_bp.route('/update_consumekafka/', methods=['GET', 'OPTIONS'])
async def update_consumekafka():
    UserId = 152
    user_processor_list = await get_processors_list(UserId)
    for processor in user_processor_list:
        if processor['Name'] == 'ConsumeKafka_2_6':
            version = processor['Version']
            break
    print(version)
    # postion의 x,y 좌표는 받아올수있으므로
    position = {
      "x": 600,
      "y": 500
    }
    topic = "user1_device5"
    groupId = "user1_device5"
    offset = "latest"
    response = await update_consumekafka_processor(version,position=position, topic=None, groupId=None, offset=None)
    response = await rule_set_default()
    return response

# putmongo 수정하기
@main_bp.route('/update_putmongo/', methods=['GET', 'OPTIONS'])
async def update_putmongo():
    UserId = 152
    user_processor_list = await get_processors_list(UserId)
    for processor in user_processor_list:
        if processor['Name'] == 'PutMongo':
            version = processor['Version']
            break
    print(version)
    # postion의 x,y 좌표는 받아올수있으므로
    position = {
      "x": 800,
      "y": 500
    }
    # 기존에 존재하는 Database와 Collection_Name이어야한다.
    Mongo_Database_Name = "testdb"
    Mongo_Collection_Name = "TEST_NIFI3"
    response = await update_putmongo_processor(version,position=position, Mongo_Database_Name_input=None, Mongo_Collection_Name_input =None)
    response = await rule_set_default()
    return response

# processor 삭제하기
@main_bp.route('/delete_processors/', methods=['GET', 'OPTIONS'])
async def delete_processors():
    UserId = 152
    token = await get_token()
    # 이미 processor_id를 앍고있으므로 
    
    consumkafka_id = "bbf68884-0191-1000-b740-7743289a0d42"
    putmongo_id = "baa54b56-0191-1000-2a30-c80ba7354bd3"
    user_processor_list = await get_processors_list(UserId)
    # print(user_processor_list)
    for processor in user_processor_list:
        if processor['ID'] == putmongo_id:
            version = processor['Version']
            break
    # print(version)
    client_id = await get_client_id()
    # print(client_id)
    url = f"{NIFI_URL}processors/{putmongo_id}"
    params = {
        'version': version,
        'clientId': client_id
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # 요청 보내기 전에 관계를 일단 지우자
    user_connection_list = await get_all_connection(UserId)
    # print(user_connection_list)
    # 관계는 누군가의 출발점이자 누군가의 도착점이으로 2개조회
    processor_connection_info = [
    {
        "Connection ID": connection['Connection ID'],
        "Version": connection['Version']
    }
    for connection in user_connection_list
    if connection['Destination Processor ID'] == putmongo_id or connection['Source Processor ID'] == putmongo_id
    ]


    # print(processor_connection_info)
    # 이제 관계를 끊기
    
    for i in range(len(processor_connection_info)):
        connection_id = processor_connection_info[i]["Connection ID"]
        version = processor_connection_info[i]["Version"]
        await delete_connections(connection_id, version)


    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.delete(url, headers=headers, params=params)
            response_text = response.text
            if response.status_code == 200:  # 성공적으로 삭제되었을 경우
                # return jsonify({"message": "Processor deleted successfully", "response": response_text}), 200
                response = await rule_set_default()
                return response
            else:
                return jsonify({"error": "Failed to delete processor", "details": response_text}), response.status_code
    except Exception as e:
        print(f"An error occurred while deleting the processor: {e}")
        return jsonify({"error": "An error occurred while deleting the processor", "details": str(e)}), 500
    # return jsonify(200)



# connection 삭제하기
@main_bp.route('/delete_connections/', methods=['GET', 'OPTIONS'])
async def delete_connections(connection_id,version):
    UserId = 152
    token = await get_token()
    # version, token, client_id, conneciton_id
    client_id = await get_client_id()
    # print(client_id)
    url = f"{NIFI_URL}connections/{connection_id}"
    params = {
        'version': version,
        'clientId': client_id
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.delete(url, headers=headers, params=params)
            response_text = response.text
            if response.status_code == 200:  # 성공적으로 삭제되었을 경우
                return jsonify({"message": "Processor deleted successfully", "response": response_text}), 200
            else:
                return jsonify({"error": "Failed to delete processor", "details": response_text}), response.status_code
    except Exception as e:
        print(f"An error occurred while deleting the processor: {e}")
        return jsonify({"error": "An error occurred while deleting the processor", "details": str(e)}), 500
    # return jsonify(200)