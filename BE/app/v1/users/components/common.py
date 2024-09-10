from contextlib import asynccontextmanager
from quart import jsonify, request, Response
from app.models.model import *
from sqlalchemy.future import select
import bcrypt # type: ignore 
import jwt
import json
import secrets
from datetime import datetime, timedelta
from types import SimpleNamespace


# 비동기 컨텍스트 관리자
@asynccontextmanager


# 데이터 베이스 세션 함수화
async def get_session():
    async with async_session() as session:
        yield session


# 프리플라이트 요청 처리
async def preflight_request():
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request"}), 200
    return None 


# JSON 데이터 유효성 검사
async def json_validation(require_name=True):
    try:
        req = await request.get_json()

        name = req.get("name") if require_name else None
        email = req.get("email")
        pwd = req.get("password")
        
        missing_fields = []
        if require_name and not name:
            missing_fields.append("이름")
        if not email:
            missing_fields.append("이메일")
        if not pwd:
            missing_fields.append("패스워드")

        if missing_fields:
            return False, Response(
                json.dumps({"error": f"{', '.join(missing_fields)}은(는) 필수 항목입니다."}, ensure_ascii=False), 
                status=400, 
                content_type="application/json"
            )

        req = SimpleNamespace(name=name, email=email, pwd=pwd)
        return True, req
    
    except Exception as e:
        return False, Response(
            json.dumps({"error": "JSON 유효성 검사 중 오류가 발생했습니다.", "details": str(e)}, ensure_ascii=False), 
            status=500, 
            content_type="application/json"
        )
    

# 이메일로 사용자 정보 가져오기
async def get_email(email):
    async with get_session() as session:
        search = await session.execute(select(UserInfo).where(UserInfo.UserEmail == email))
        return search.scalar()


# UserID로 user_process_group_id 가져오기
async def get_user_process_group_id(UserID):
    async with get_session() as session:
        search = await session.execute(select(UserPGInfo.PgID).where(UserPGInfo.UserID == UserID))
        # 일단은 1개 반환 
        # pg_ids = search.scalars().all()
        return search.scalar()  




# 비밀번호 해시화 및 문자열 변환
async def hashed_password(pwd):
    # 비밀번호를 utf-8로 인코딩하여 바이트 스트림으로 변환
    hashed_pwd = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())
    # 해시된 비밀번호를 utf-8로 디코딩하여 저장 (DB에 문자열로 저장하기 위함)
    serializable_pwd = hashed_pwd.decode("utf-8")
    return hashed_pwd, serializable_pwd


# 비밀번호 검증 
async def verify_password(user_info, pwd):
    try:
        # 클라이언트로부터 받은 비밀번호를 utf-8로 인코딩 (bytes)
        encoded_pwd = pwd.encode("utf-8")
        # 바이트 스트림끼리 비교한다. 해시값은 매번 변하지만 salt는 고유
        check_pwd = bcrypt.checkpw(encoded_pwd, user_info.UserPwd.encode("utf-8"))

        # 비밀번호 검증
        if check_pwd:
            return True, None, 200
        else:
            # 비밀번호가 일치하지 않을 경우
            return False, jsonify({"error": "패스워드가 일치하지 않습니다."}), 400
    except Exception as e:
        return False, jsonify({"error": "비밀번호 검증 중 오류가 발생했습니다.", "details": str(e)}), 500
        

# 유저 ID로 토큰 정보 가져오기
async def get_token_info(email):
    async with get_session() as session:
        result = await get_email(email)
        search_token = await session.execute(select(JwtInfo).where(JwtInfo.UserID == result.UserID))
        return search_token.scalar()


# 토큰 생성
async def create_token(email):

    # 사용자 정보 가져오기
    search_user = await get_email(email)

    if not search_user:
        return None
    
    user_email = search_user.UserEmail

    # 현재 시간 정의
    issued_time = datetime.now() + timedelta(hours=9)
    expiry_time = issued_time + timedelta(hours=1)
    payload = {
        "email" : user_email,
        "issuedAt" : issued_time.isoformat(),
        "expiryAt" : expiry_time.isoformat()
    }
    JWT_SECRET_KEY = secrets.token_urlsafe(32)
    # 토큰 생성
    token = jwt.encode(payload, JWT_SECRET_KEY, "HS256")
    return token
            

# 토큰 갱신
async def verify_token(email):
    async with get_session() as session:

        # 토큰 정보 가져오기
        update_token = await get_token_info(email)
        
        if not update_token:
            return None
        
        token = await create_token(email)

        issued_time = datetime.now() + timedelta(hours=9)
        expiry_time = issued_time + timedelta(minutes=30)

        if update_token:
                update_token.AccessToken = token
                update_token.IssuedAt = issued_time
                update_token.ExpiryAt = expiry_time
                await session.commit()

                return token


# 신규 토큰 DB 삽입
async def new_insert_token(id, token):
    async with get_session() as session:
        if not token:
            return False, jsonify({"error": "토큰 생성 중 오류가 발생했습니다."}), 500

        try:
            # 토큰 정보를 데이터베이스에 저장
            new_token = JwtInfo(
                UserID=id,
                AccessToken=token, 
                IssuedAt=datetime.now() + timedelta(hours=9), 
                ExpiryAt=datetime.now() + timedelta(hours=9) + timedelta(hours=1)
            )
            session.add(new_token)
            await session.commit()
            return True, jsonify({"message": "토큰이 성공적으로 저장되었습니다."}), 200

        except Exception as e:
            await session.rollback()  # 트랜잭션 롤백
            return False, jsonify({"error": "토큰 삽입 중 오류가 발생했습니다.", "details": str(e)}), 500