from quart import jsonify
from app.models.model import *
from sqlalchemy.future import select
from .common import *

async def create_user(email, name, pwd):
    async with get_session() as session:
        
        # 이메일로 사용자 정보 가져오기
        user_info = await get_email(email)
        if user_info is not None:
            return False, jsonify({"error": "중복된 이메일입니다."}), 400
        
        # 비밀번호 해시화
        _, serializable_pwd = await hashed_password(pwd)

        # 새로운 사용자 생성
        new_user = UserInfo(UserNm=name, UserEmail=email, UserPwd=serializable_pwd)

        try:
            # 회원 정보 DB 삽입
            session.add(new_user)
            await session.commit()

            # 신규 토큰 생성
            token = await create_token(email)
            
            # 회원가입 한 유저의 id 값 가져오기 
            id = await get_email(email)

            # 신규 토큰 DB 삽입
            success, created, status_code = await new_insert_token(id.UserID, token)
            
            if not success:
                return success, created, status_code

            # 고객 정보 및 생성된 토큰 반환
            return True, jsonify({
                "email" : new_user.UserEmail,
                "name" : new_user.UserNm,
                "access_token" : token
            }), 201
        
        except Exception as e:
            await session.rollback()  # 트랜잭션 롤백

            return False, jsonify({"error": "사용자 생성 중 오류가 발생했습니다.", "details": str(e)}), 500
    
async def login_validation(email, pwd):

        user_info = await get_email(email)
        if user_info is None:
            return False, jsonify({"error": "존재하지 않는 이메일입니다."}), 400

        # 패스워드 검증
        success, response, status_code = await verify_password(user_info, pwd)

        if not success:
            return success, response, status_code

        try:
            token_info = await get_token_info(email)
        
            # 발행된 토큰이 없을 경우 신규 토큰 생성
            if not token_info:

                token = await create_token(email)

                # 신규 토큰 DB 삽입
                success, created, status_code = await new_insert_token(token_info.UserID, token)
                
                if not success:
                    return success, created, status_code
                
                return True, jsonify({
                    "email" : email,
                    "name" : user_info.UserNm,
                    "access_token" : token
                }), 201

            issued_time = datetime.now() + timedelta(hours=9)

            # 토큰 갱신 (만료 시간이 30분 이하로 남은 경우)
            if token_info.ExpiryAt - issued_time <= timedelta(minutes=30):
                token = await verify_token(email)
                return  True, jsonify({
                    "email" : email, 
                    "name" : user_info.UserNm,
                    "access_token" : token
                }), 201
            
            return True, jsonify({
                "email" : email, 
                "name" : user_info.UserNm,
                "access_token" :token_info.AccessToken
            }), 200
        
        except Exception as e:
            return False, jsonify({"error": "사용자 생성 중 오류가 발생했습니다.", "details": str(e)}), 500
    



        