from quart import Blueprint, request, jsonify, current_app
from app.models.model import UserInfo, JwtInfo, async_session
from sqlalchemy.future import select
import base64
import bcrypt # type: ignore
import jwt
from datetime import datetime, timedelta


login_bp = Blueprint('login',__name__)

@login_bp.route('/login/', methods=['POST', 'OPTIONS'])
async def login():
    async with async_session() as session:

        # requests 정보 매핑
        req = await request.get_json()

        # JSON 데이터 유효성 검사
        if req is None:
            return jsonify({"error": "요청에 잘못된 또는 누락된 JSON이 있습니다."}), 400
        
        email = req.get("email")
        pwd = req.get("password")
        encoded_pwd = base64.b64encode(pwd.encode("utf-8"))

        # eamil을 통한 사용자 정보 불러오기
        search = await session.execute(select(UserInfo).where(UserInfo.UserEmail == email))
        result = search.scalar()

        # email 존재하지 않을 경우
        if not result:
            return jsonify({"error": "존재하지 않는 이메일입니다."}), 401

        # 패스워드 일치 여부 확인
        if not bcrypt.checkpw(encoded_pwd, result.UserPwd.encode("utf-8")):
            return jsonify({"error": "패스워드가 일치하지 않습니다."}), 402
        
        # UserID를 통한 토큰 정보 불러오기
        search_token = await session.execute(select(JwtInfo).where(JwtInfo.UserID == result.UserID))
        result_token = search_token.scalar()

        # 현재 시간 정의
        issued_time = datetime.now() + timedelta(hours=9)

        # 토큰이 없을 때 생성하기
        if not result_token:
            
            expiry_time = issued_time + timedelta(hours=1)

            payload = {
                "email" : email,
                "issuedAt" : issued_time.isoformat(),
                "expiryAt" : expiry_time.isoformat()
            }

            # 토큰 생성
            token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], "HS256")

            # 생성 토큰한 토큰 DB insert
            new_token = JwtInfo(UserID=result.UserID, AccessToken=token, IssuedAt=issued_time, ExpiryAt=expiry_time)
            session.add(new_token)
            await session.commit()
            
            return jsonify({
                "email" : result.UserEmail,
                "name" : result.UserNm,
                "access_token" : token
            })


        # 잔여시간이 30분 이하일 경우 토큰 만료시간을 30분으로 갱신
        if result_token.ExpiryAt >= issued_time and result_token.ExpiryAt - issued_time <= timedelta(minutes=30):

            expiry_time = issued_time + timedelta(hours=30)

            payload = {
                "email" : email,
                "issuedAt" : issued_time.isoformat(),
                "expiryAt" : expiry_time.isoformat()
            }

            # 재발급 토큰 생성
            token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], "HS256")

            # 기존 토큰 정보 갱신
            update_token = await session.execute(select(JwtInfo).where(JwtInfo.UserID == result.UserID))
            update_token = update_token.scalar()

            if update_token:
                update_token.AccessToken = token
                update_token.IssuedAt = issued_time
                update_token.ExpiryAt = expiry_time
                await session.commit()

                return  jsonify({
                    "email" : result.UserEmail,
                    "name" : result.UserNm,
                    "access_token" : token
                    })
            
        # 토큰 시간이 만료되었을 경우             
        if result_token.ExpiryAt < issued_time:
            return jsonify({"error": "토큰 시간이 만료되었습니다. 다시 로그인 해주세요."}), 403
            
        # JwtInfo Table에 생성되어 있는 토큰 정보 반환
        return  jsonify({
                    "email" : result.UserEmail,
                    "name" : result.UserNm,
                    "access_token" : result_token.AccessToken
                    })
        
