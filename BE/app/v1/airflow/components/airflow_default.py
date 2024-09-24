# 비동기 방식으로 Airflow에 POST 요청 보내기
import httpx
import base64
from dotenv import load_dotenv
import os


# .env 파일 로드
load_dotenv("/etc/airflow_ip.env")
# Airflow의 프라이빗 IP 가져오기
AIRFLOW_PRIVATE_IP = os.getenv("AIRFLOW_PRIVATE_IP")
# Airflow API URL 설정
AIRFLOW_BASE_URL = f"http://{AIRFLOW_PRIVATE_IP}:8080/api/v1/dags"

USERNAME = os.getenv("AIRFLOW_USERNAME") # 이미지에서 제공된 사용자 이름
PASSWORD = os.getenv("AIRFLOW_PASSWORD")  # 이미지에서 제공된 비밀번호

# Basic Auth 헤더 생성
def create_basic_auth_header(username, password):
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode('utf-8')
    return f"Basic {encoded_credentials}"

# 비동기 방식으로 Airflow에 POST 요청 보내기
async def trigger_dag_run(dag_id, conf):
    url = f"{AIRFLOW_BASE_URL}/{dag_id}/dagRuns"
    headers = {
        "Content-Type": "application/json",
        "Authorization": create_basic_auth_header(USERNAME, PASSWORD)  # Basic Auth 헤더 추가
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"conf": conf}, headers=headers)
    return response
