from quart import Blueprint, request, jsonify
from dotenv import load_dotenv
from quart import jsonify, Response  

import os
import httpx
from app.v1.users.components.common import *
import aiohttp
from app.v1.nifi.components.nifi_default import *


nifi_api_bp = Blueprint('nifi_api', __name__)
load_dotenv()
Mongo = os.getenv("Mongo")
NIFI_URL = os.getenv("NIFI_URL") #https://192.168.1.234:8443/nifi-api/ 
Mongo_URI = os.getenv("Mongo_URI")
Mongo_Database_Name = os.getenv("Mongo_Database_Name")
Mongo_Collection_Name = os.getenv("Mongo_Collection_Name")

# consumkafka 생성 http://localhost:19020/v1/nifi_api/make_consumekafka/
@nifi_api_bp.route('/make_consumekafka/', methods=['GET', 'OPTIONS'])
async def create_consumekafka_processor():
    # token, user_process_group_id
    token = await get_token()
    user_process_group_id = await get_user_process_group_id(152)
    print(user_process_group_id)   
    url = f"{NIFI_URL}process-groups/{user_process_group_id}/processors"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    body = {
        "revision": {
    "version": 0
  },
  "component": {
    "type": "org.apache.nifi.processors.kafka.pubsub.ConsumeKafka_2_6",
    "bundle": {
      "group": "org.apache.nifi",
      "artifact": "nifi-kafka-2-6-nar",
      "version": "1.20.0"
    },
    "name": "ConsumeKafka_2_6",
    "position": {
      "x": 500,
      "y": 500
    },
    "config": {
      "properties": {
        "bootstrap.servers": Mongo,
        "topic": "user1_device5",
        "group.id": "test_group2",
        "auto.offset.reset": "earliest",
        "key.deserializer": "org.apache.kafka.common.serialization.StringDeserializer",
        "value.deserializer": "org.apache.kafka.common.serialization.StringDeserializer"
      },
      "autoTerminatedRelationships": ["failure", "success"]
    }
  } 
    }
    
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, headers=headers, json=body)
            response_text = response.text
            if response.status_code == 200:  # 성공적으로 생성되었을 경우
                return jsonify({"message": "Processor created successfully", "response": response_text}), 200
            else:
                return jsonify({"error": "Failed to create processor", "details": response_text}), response.status_code
    except Exception as e:
        print(f"An error occurred while creating the processor: {e}")
        return jsonify({"error": "An error occurred while creating the processor", "details": str(e)}), 500


# consumkafka 수정 http://localhost:19020/v1/nifi_api/update_consumekafka/
# @nifi_api_bp.route('/update_consumekafka/', methods=['GET', 'OPTIONS'])
async def update_consumekafka_processor(version,position=None, topic=None, groupId=None, offset=None):
    # token, user_process_group_id
    token = await get_token()
    # web 상에서 클릭하면 id정보과 우측에 뜨므로
    processor_id = "baa559ac-0191-1000-0d61-b9fcba30dde2"
    url = f"{NIFI_URL}processors/{processor_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # version 받기
    body = {
        "revision": {
            "version": version
        },
        "component": {
            "id" : processor_id,
            "type": "org.apache.nifi.processors.kafka.pubsub.ConsumeKafka_2_6",
            "bundle": {
            "group": "org.apache.nifi",
            "artifact": "nifi-kafka-2-6-nar",
            "version": "1.20.0"
        },
        "name": "ConsumeKafka_2_6",
        "position": position,
        "config": {
            "properties": {
                "bootstrap.servers": Mongo,
                "topic": topic,
                "group.id": groupId,
                "auto.offset.reset": offset,
                "key.deserializer": "org.apache.kafka.common.serialization.StringDeserializer",
                "value.deserializer": "org.apache.kafka.common.serialization.StringDeserializer"
                },
            "autoTerminatedRelationships": ["failure"]
            }
        } 
    }
    
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.put(url, headers=headers, json=body)
            response_text = response.text
            if response.status_code == 200:  # 성공적으로 생성되었을 경우
                return jsonify({"message": "Processor created successfully", "response": response_text}), 200
            else:
                return jsonify({"error": "Failed to create processor", "details": response_text}), response.status_code
    except Exception as e:
        print(f"An error occurred while creating the processor: {e}")
        return jsonify({"error": "An error occurred while creating the processor", "details": str(e)}), 500
    # return jsonify(200)


# putmongo 생성하기 http://localhost:19020/v1/nifi_api/make_putmongo/
@nifi_api_bp.route('/make_putmongo/', methods=['GET', 'OPTIONS'])
async def create_putmongo_processor():
    # NIFI_URL = load_env()['NIFI_URL']
    token = await get_token()
    user_process_group_id = await get_user_process_group_id(152)
    print(user_process_group_id)   
    url = f"{NIFI_URL}process-groups/{user_process_group_id}/processors"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    body = {
        "revision": {
            "version": 0
        },
        "component": {
            "type": "org.apache.nifi.processors.mongodb.PutMongo",
            "name": "PutMongo",
            "position": {
                "x": 584,
                "y": 152
            },
            "config": {
                "properties": {
                    "Mongo URI": Mongo_URI, 
                    "Mongo Database Name": Mongo_Database_Name, # 이름
                    "Mongo Collection Name": Mongo_Collection_Name, # 컬렉션
                    "ssl-client-auth": "REQUIRED",
                    "Mode": "insert",
                    "Upsert": "false",
                    "Update Query Key": None,
                    "putmongo-update-query": None,
                    "put-mongo-update-mode": "doc",
                    "Write Concern": "ACKNOWLEDGED",
                    "Character Set": "UTF-8"
                },
                "autoTerminatedRelationships": ["failure", "success"],
                "schedulingPeriod": "0 sec",
                "penaltyDuration": "30 sec",
                "yieldDuration": "1 sec",
                "executionNode": "ALL",
                "bulletinLevel": "WARN",
                "runDurationMillis": 0,
                "concurrentlySchedulableTaskCount": 1,
                "comments": "",
                "lossTolerant": False,
                "defaultConcurrentTasks": {
                    "TIMER_DRIVEN": "1",
                    "EVENT_DRIVEN": "0",
                    "CRON_DRIVEN": "1"
                },
                "defaultSchedulingPeriod": {
                    "TIMER_DRIVEN": "0 sec",
                    "CRON_DRIVEN": "* * * * * ?"
                },
                "retryCount": 10,
                "retriedRelationships": [],
                "backoffMechanism": "PENALIZE_FLOWFILE",
                "maxBackoffPeriod": "10 mins"
            }
        }
    }
    
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, headers=headers, json=body)
            response_text = response.text
            if response.status_code == 200:  # 성공적으로 생성되었을 경우
                return jsonify({"message": "Processor updated successfully", "response": response_text}), 200
            else:
                return jsonify({"error": "Failed to update processor", "details": response_text}), response.status_code
    except Exception as e:
        print(f"An error occurred while updating the processor: {e}")
        return jsonify({"error": "An error occurred while updating the processor", "details": str(e)}), 500


# putmongo 수정 http://localhost:19020/v1/nifi_api/update_putmongo/
# @nifi_api_bp.route('/update_putmongo/', methods=['GET', 'OPTIONS'])
async def update_putmongo_processor(version,position=None, Mongo_Database_Name_input=None, Mongo_Collection_Name_input=None):
    # token, user_process_group_id
    token = await get_token()
    # web 상에서 클릭하면 id정보과 우측에 뜨므로
    processor_id = "baa54b56-0191-1000-2a30-c80ba7354bd3"
    url = f"{NIFI_URL}processors/{processor_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # version 받기
    body = {
        "revision": {
            "version": version
        },
        "component": {
            "id" : processor_id,
            "type": "org.apache.nifi.processors.mongodb.PutMongo",
            "name": "PutMongo",
            "position": position,
            "config": {
                "properties": {
                    "Mongo URI": Mongo_URI, 
                    "Mongo Database Name": Mongo_Database_Name_input, # 이름
                    "Mongo Collection Name": Mongo_Collection_Name_input, # 컬렉션
                    "ssl-client-auth": "REQUIRED",
                    "Mode": "insert",
                    "Upsert": "false",
                    "Update Query Key": None,
                    "putmongo-update-query": None,
                    "put-mongo-update-mode": "doc",
                    "Write Concern": "ACKNOWLEDGED",
                    "Character Set": "UTF-8"
                },
                "autoTerminatedRelationships": ["failure", "success"],
                "schedulingPeriod": "0 sec",
                "penaltyDuration": "30 sec",
                "yieldDuration": "1 sec",
                "executionNode": "ALL",
                "bulletinLevel": "WARN",
                "runDurationMillis": 0,
                "concurrentlySchedulableTaskCount": 1,
                "comments": "",
                "lossTolerant": False,
                "defaultConcurrentTasks": {
                    "TIMER_DRIVEN": "1",
                    "EVENT_DRIVEN": "0",
                    "CRON_DRIVEN": "1"
                },
                "defaultSchedulingPeriod": {
                    "TIMER_DRIVEN": "0 sec",
                    "CRON_DRIVEN": "* * * * * ?"
                },
                "retryCount": 10,
                "retriedRelationships": [],
                "backoffMechanism": "PENALIZE_FLOWFILE",
                "maxBackoffPeriod": "10 mins"
            }
        }
    }
    
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.put(url, headers=headers, json=body)
            response_text = response.text
            if response.status_code == 200:  # 성공적으로 생성되었을 경우
                return jsonify({"message": "Processor updated successfully", "response": response_text}), 200
            else:
                return jsonify({"error": "Failed to update processor", "details": response_text}), response.status_code
    except Exception as e:
        print(f"An error occurred while updating the processor: {e}")
        return jsonify({"error": "An error occurred while updating the processor", "details": str(e)}), 500
    # return jsonify(200)




# 프로세서그룹안에있는 프로세서 목록 가져오기 http://localhost:19020/v1/nifi_api/get_process_list/
@nifi_api_bp.route('/get_process_list/', methods=['GET', 'OPTIONS'])
async def get_processors_list(UserId):
    token = await get_token()
    user_process_group_id = await get_user_process_group_id(UserId)
    url = f"{NIFI_URL}process-groups/{user_process_group_id}/processors"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, headers=headers)
            
            parsed_data = []
            for processor in response.json()['processors']:
                component = processor['component']
                processor_info = {
                    "ID": component['id'],
                    "Name": component['name'],
                    "Type": component['type'],
                    "Properties": component['config']['properties'],
                    "Version": processor['revision']['version'],
                    "Position": {
                        "x": component['position']['x'],
                        "y": component['position']['y']
                    }
                }
                parsed_data.append(processor_info)
            # print(parsed_data)
            return parsed_data
            # return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": "Failed to get processor list", "details": str(e)}), 500

# 두개의 프로세서 연결하기 http://localhost:19020/v1/nifi_api/create_connection/
@nifi_api_bp.route('/create_connection/', methods=['GET', 'OPTIONS'])
async def create_connection():
    # temp_process_group_id,token,first_processor_id,second_processor_id
    token = await get_token()
    # user_group_id 가져오기
    user_process_group_id = await get_user_process_group_id(152)
    
    # 임의로 137번의 프로세서 목록가져오기
    # ids = [processor['ID'] for processor in await get_processors_list()]

    processors_response = await get_processors_list()

    # JSON 데이터를 파싱
    processors = await processors_response.get_json()  # Response 객체에서 JSON 데이터 추출

    # processors에서 각 ID와 Version을 추출
    ids = [processor['ID'] for processor in processors]
    print(ids)
    url = f'{NIFI_URL}process-groups/{user_process_group_id}/connections'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    data = {
        "revision": {
            "version": 0
        },
        "component": {
            "source": {
                "id": ids[1],
                "groupId": user_process_group_id,
                "type": "PROCESSOR"
            },
            "destination": {
                "id": ids[0],
                "groupId": user_process_group_id,
                "type": "PROCESSOR"
            },
            "name": "ConsumeKafka_to_PutMongo",
            "labelIndex": 0,
            "zIndex": 0,
            "selectedRelationships": [
                "success",
            ],
            "availableRelationships": [
                "success",
                "failure"
            ]
        }
    }
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return jsonify({"message": "Connection created successfully", "response": response.json()}), 200
            else:
                return jsonify({"error": "Failed to create connection", "details": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": "An error occurred while creating the connection", "details": str(e)}), 500


# 프로세서 run상태로하기 http://localhost:19020/v1/nifi_api/create_connection/
@nifi_api_bp.route('/run_status/', methods=['GET', 'OPTIONS'])
async def set_processor_run_status():
    # processor_id, token, state, version
    token = await get_token()
    # user_group_id 가져오기
    user_process_group_id = await get_user_process_group_id(152)

    # processors를 JSON으로 받음
    processors_response = await get_processors_list()

    # JSON 데이터를 파싱
    processors = await processors_response.get_json()  # Response 객체에서 JSON 데이터 추출

    # processors에서 각 ID와 Version을 추출
    ids = [processor['ID'] for processor in processors]
    versions = [processor['Version'] for processor in processors]

    # 여기서 for문으로 돌림 앞에서부터 순서대로
    print(ids)
    print(versions)

    for id, version in zip(ids, versions):
        url = f'{NIFI_URL}processors/{id}/run-status'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        data = {
            "revision": {
                "version": version  # 올바른 버전을 사용
            },
            "state": "RUNNING"  
        }

        async with httpx.AsyncClient(verify=False) as client:
            response = await client.put(url, headers=headers, json=data)
            print(response.status_code, response.text)  

    return jsonify({"message": "Processors run status updated successfully", "ids": ids})



# 프로세서 관계 전체 들고오기 http://localhost:19020/v1/nifi_api/get_all_connection/
@nifi_api_bp.route('/get_all_connection/', methods=['GET', 'OPTIONS'])
async def get_all_connection(UserId):
    token = await get_token()
    user_process_group_id = await get_user_process_group_id(UserId)
    url = f"{NIFI_URL}process-groups/{user_process_group_id}/connections"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, headers=headers)
            connections = response.json().get('connections', [])
            
            parsed_data = []
            for connection in connections:
                connection_info = {
                    "Connection ID": connection['component']['id'],
                    "Source Processor ID": connection['component']['source']['id'],
                    "Source Processor Name": connection['component']['source']['name'],
                    "Destination Processor ID": connection['component']['destination']['id'],
                    "Destination Processor Name": connection['component']['destination']['name'],
                    "Version": connection['revision']['version']
                }
                parsed_data.append(connection_info)

            # return parsed_data
            return parsed_data

    except Exception as e:
        return jsonify({"error": "Failed to get processor list", "details": str(e)}), 500

# consumkafka 생성 http://localhost:19020/v1/nifi_api/make_custom_consumekafka/
@nifi_api_bp.route('/make_custom_consumekafka/', methods=['GET', 'OPTIONS'])
async def create_custom_consumekafka_processor():
    # token, user_process_group_id
    token = await get_token()
    # user_process_group_id = await get_user_process_group_id(152)
     # test용
    user_process_group_id = "3165600b-0191-1000-53ce-3b268028503c"
    print(user_process_group_id)   
    url = f"{NIFI_URL}process-groups/{user_process_group_id}/processors"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    body = {
    "revision": {
        "version": 0
    },
    "component": {
        "name": "My Custom Kafka Processor",
        "type": "com.example.nifi.MyProcessor",
        "config": {
            "properties": {
                "Topic Name": "user3_device1",
                "Group ID": "nifi1",
                "Auto Offset Reset": "earliest"
            },
            "schedulingPeriod": "1 sec",
            "autoTerminatedRelationships": ["FAILURE","SUCCESS"],
            "schedulingStrategy": "TIMER_DRIVEN",
            "penaltyDuration": "30 sec",
            "yieldDuration": "1 sec",
            "bulletinLevel": "WARN",
            "runDurationMillis": 0,
        },
        "position": {
            "x": 500,
            "y": 500
        }
    }
}

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, headers=headers, json=body)
            response_text = response.text
            if response.status_code == 200:  # 성공적으로 생성되었을 경우
                return jsonify({"message": "Processor created successfully", "response": response_text}), 200
            else:
                return jsonify({"error": "Failed to create processor", "details": response_text}), response.status_code
    except Exception as e:
        print(f"An error occurred while creating the processor: {e}")
        return jsonify({"error": "An error occurred while creating the processor", "details": str(e)}), 500


# kafka_streaming 생성 http://localhost:19020/v1/nifi_api/make_custom_kafka_streaming/
@nifi_api_bp.route('/make_custom_kafka_streaming/', methods=['GET', 'OPTIONS'])
async def create_custom_kafka_streaming_processor():
    # token, user_process_group_id
    token = await get_token()
    # user_process_group_id = await get_user_process_group_id()
    # test용
    user_process_group_id = "3165600b-0191-1000-53ce-3b268028503c"
    print(user_process_group_id)   
    url = f"{NIFI_URL}process-groups/{user_process_group_id}/processors"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    body = {
    "revision": {
        "version": 0
    },
    "component": {
        "name": "My Custom Kafka Processor",
        "type": "com.example.nifi.kafka.streaming.MyProcessor",
        "config": {
            "properties": {
                "BOOTSTRAP_SERVERS": "test",
                "User Rule": "test",
                "Application ID": "test",
                "Topic Name": "test",
            },
            "schedulingPeriod": "1 sec",
            "autoTerminatedRelationships": ["FAILURE","SUCCESS"],
            "schedulingStrategy": "TIMER_DRIVEN",
            "penaltyDuration": "30 sec",
            "yieldDuration": "1 sec",
            "bulletinLevel": "WARN",
            "runDurationMillis": 0,
        },
        "position": {
            "x": 500,
            "y": 500
        }
    }
}

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, headers=headers, json=body)
            response_text = response.text
            if response.status_code == 200:  # 성공적으로 생성되었을 경우
                return jsonify({"message": "Processor created successfully", "response": response_text}), 200
            else:
                return jsonify({"error": "Failed to create processor", "details": response_text}), response.status_code
    except Exception as e:
        print(f"An error occurred while creating the processor: {e}")
        return jsonify({"error": "An error occurred while creating the processor", "details": str(e)}), 500

