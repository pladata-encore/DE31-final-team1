## 젠킨스(jenkins)를 통한 배포 자동화
1. 로컬 작업 브랜치(feature branch)를 게시 
2. gihub에서 Pull requests를 통해 2명 이상의 리뷰어가 승인
3. 요청자가 feature branch와 develop를 merge 
4. Trigger : merge가 발생된 시점

## 로컬 실행 명령어

    # 1회성 실행  
    docker-compose up --build 

    # bg 실행  
    docker-compose up --build -d 

    # 이미 빌드한 container가 존재할 경우  
    docker start [컨테이너명]

## 로컬에서의 실행 환경

- docker-compose를 통해 build
- python3 
    - ubuntu에 설치되어 있는 기본 python3 
    - /usr/bin/python3
- .venv 환경을 사용하지 않음(로컬에서 개인적으로 테스트할 때는 사용)

