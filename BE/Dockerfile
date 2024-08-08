# 베이스 이미지 정의
FROM ubuntu:22.04

# 서울 시간대로 변경
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# sudo 사용을 위해 사용자 추가
RUN useradd -m -s /bin/bash mydir && \
    echo "mydir ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 작업 디렉토리 설정
WORKDIR /home/mydir/api-server

# 시스템 호스트 볼륨 마운트
VOLUME /home/mydir/api-server

# 현재 폴더 내의 파일 모두 복사 
COPY . /home/mydir/api-server

# 가상환경 & 패키지 설치
RUN apt update && \
    apt -y install python3.10 python3-venv python3-pip && \
    . /home/mydir/api-server/.venv/bin/activate && pip install -r requirements.txt 

# Flask 환경 변수를 설정합니다.
ENV FLASK_APP=run.py

# 포트 설정
EXPOSE 5000

CMD ["/home/mydir/api-server/.venv/bin/python", "run.py", "--host=0.0.0.0", "--port=5000"]