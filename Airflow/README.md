# Airflow in docker compose
    - 배치성 데이터 파이프라인 관리를 위해 airflow 구축
    - 스케줄링, 모니터링이 가능한 워크플로우 관리 도구
## 실행 단계
1. 권한 설정 스크립트 실행
```./setup_permission.sh```
2. Docker compose 실행
```docker compose up -d```

### Apache Airflow 구성 요소
1. **Scheduler**
    - 작업의 실행 순서 및 스케줄을 관리합니다.
    - DAG(Directed Acyclic Graph) 스케줄링을 통해 복잡한 워크플로우를 자동으로 실행합니다.
2. **Web Server**
    - 사용자 인터페이스를 제공하여 DAG 및 태스크 상태를 시각적으로 관리할 수 있습니다.
    - 워크플로우의 상태, 로그, 메트릭 등을 실시간으로 모니터링할 수 있습니다.
3. **Worker**
    - 실제 태스크를 실행하는 컴포넌트입니다.
    - CeleryExecutor와 같은 분산 실행 환경을 통해 대규모 작업 처리를 지원합니다.
4. **Metadata Database**
    - DAG 및 태스크의 상태, 실행 이력 등을 저장합니다.
    - 구현한 Airflow에서는 PostgreSQL 관계형 데이터베이스를 사용합니다.
5. **DAGs (Directed Acyclic Graphs)**
    - 워크플로우의 각 단계를 정의한 파이프라인입니다.
    - Python 코드로 작성되며, 태스크 간의 종속성을 명확하게 정의합니다