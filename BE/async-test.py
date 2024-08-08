######################################################
# Docker container를 먼전 실행 한 뒤 비동기 코드를 실행해주세요 #
######################################################

import asyncio
import aiohttp
import time

# post 요청 함수 정의
async def send_post_request(url, payload):
    async with aiohttp.ClientSession() as session:
        
        # 시작 시간 할당
        start_time = time.time()
        async with session.post(url, json=payload) as response:
            response_text = await response.text()
            # 완료 시간 할당
            end_time = time.time()

            # 소요 시간 
            elapsed_time = end_time - start_time
            print(f"{payload['name']}: {response_text} (소요 시간: {elapsed_time:.2f} 초)")
            return response_text, elapsed_time

# get 요청 함수 정의
async def send_get_request(url, payload):
    async with aiohttp.ClientSession() as session:
        
        # 시작 시간 할당
        start_time = time.time()
        async with session.get(url) as response:
            response_text = await response.text()

            # 완료 시간 할당
            end_time = time.time()

            # 소요 시간 
            elapsed_time = end_time - start_time

            if response.status == 200:
                response_text = await response.text()
                print(f"GET 요청 반환: {payload['name']} (소요 시간: {elapsed_time:.2f} 초)")
                return response_text, elapsed_time
            else:
                print(f"GET 요청 반환: {payload['name']} (소요 시간: {elapsed_time:.2f} 초)")
                return None, elapsed_time


# 메인 실행 함수
async def main():
    base_url = "http://127.0.0.1:5000/t"
    post_endpoints = ["/create1/", "/create2/", "/create3/", "/create4/"]
    get_endpoints = ["/getData/John Doe", "/getData/Jane Smith", "/getDataead1/Jake Doe", "/getData/Oba Drake"]
    payloads = [
        {"name": "John Doe"},
        {"name": "Jane Smith"},
        {"name": "Jake Doe"},
        {"name": "Oba Drake"}]
    
    print("<------------- post 측정 ------------->")

    # post 요청 보내기
    # post requests 요청 함수에 endpoint와 payloads 를 순차적으로 실행
    post_start_time = time.time()
    post_tasks = [send_post_request(f"{base_url}{endpoint}", payload) for endpoint, payload in zip(post_endpoints, payloads)]

    # 각 tasks 리스트 데이터를 언패킹하여 리스트의 각 항목을 개별 인수로 전달
    await asyncio.gather(*post_tasks)
    post_end_time = time.time()

    # 결과 출력
    # print("POST 요청 개별 완료 시간:", post_responses)
    print(f"POST 요청 전체 처리 시간 : {post_end_time - post_start_time:.2f} seconds")
    print("<------------- get 측정 ------------->")
    


    # 잠시 대기하여 데이터베이스에 데이터가 확실히 반영되도록 함
    await asyncio.sleep(1)



    # GET 요청 보내기
    # get requests 요청 함수에 endpoint와 payloads 를 순차적으로 실행
    get_start_time = time.time()
    get_tasks = [send_get_request(f"{base_url}{endpoint}", payload) for endpoint, payload in zip(get_endpoints, payloads)]

    # 각 tasks 리스트 데이터를 언패킹하여 리스트의 각 항목을 개별 인수로 전달
    await asyncio.gather(*get_tasks)
    get_end_time = time.time()

    # 결과 출력
    print(f"GET 요청 전체 처리 시간: {get_end_time - get_start_time:.2f} seconds")

    print(f"전체 처리 시간: {get_end_time - post_start_time:.2f} 초")
    print("<------------- 측정 종료 ------------->")

if __name__ == "__main__":
    asyncio.run(main())
