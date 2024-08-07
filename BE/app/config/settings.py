from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경 변수에서 데이터베이스 URL 가져오기
DATABASE_URL = os.getenv('MYSQL_URI')
if not DATABASE_URL:
    raise ValueError("MYSQL_URI 환경 변수가 설정되지 않았습니다.")