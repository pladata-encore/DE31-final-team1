#!/bin/bash

# 설정할 사용자 및 그룹 ID (컨테이너에서 사용하는 ID)
USER_ID=1001
GROUP_ID=1001

# 마운트할 디렉토리 경로
AIRFLOW_DIR="./airflow"
POSTGRESQL_DIR="$AIRFLOW_DIR/postgresql-persistence"
REDIS_DIR="$AIRFLOW_DIR/redis-persistence"
DAGS_DIR="$AIRFLOW_DIR/airflow-dags"
LOGS_DIR="$AIRFLOW_DIR/logs"
PLUGINS_DIR="$AIRFLOW_DIR/plugins"

# 디렉토리가 존재하는지 확인하고 생성
mkdir -p $POSTGRESQL_DIR
mkdir -p $REDIS_DIR
mkdir -p $DAGS_DIR
mkdir -p $LOGS_DIR
mkdir -p $PLUGINS_DIR

# 디렉토리 소유권 변경
sudo chown -R $USER_ID:$GROUP_ID $AIRFLOW_DIR

# 사용자에게 알림
echo "디렉토리 소유권이 사용자 ID $USER_ID 및 그룹 ID $GROUP_ID로 변경되었습니다."
