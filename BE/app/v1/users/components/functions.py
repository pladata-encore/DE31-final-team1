from quart import jsonify
from app.models.model import *
from sqlalchemy.future import select
from .common import *
from app.v1.nifi.nifi_api import *
from app.v1.data_group.main_dg import *

async def create_user(email, name, pwd):
    async with get_session() as session:
        
        # 이메일로 사용자 정보 가져오기
        user_info = await get_email(email)
        if user_info is not None:
            return False, jsonify({"error": "중복된 이메일입니다."}), 409
        # 비밀번호 해시화
        _, serializable_pwd = await hashed_password(pwd)

        
        # User Processor Group 생성
        # 사용자가 회원가입을 할때 추가로 생성. default로 
        pgid = await create_user_process_group()
        print(f"pgid: {pgid} (type: {type(pgid)})")
        
        # 새로운 사용자 생성
        new_user = UserInfo(UserNm=name, UserEmail=email, UserPwd=serializable_pwd)
        
        try:
            # 회원 정보 DB 삽입
            session.add(new_user)
            await session.flush()  

            # 새로운 프로세서 그룹 정보 생성
            new_group = UserPGInfo(PgID=pgid, UserID=new_user.UserID, PgName="default")
            session.add(new_group)

            await session.commit()

            # 신규 토큰 생성
            token = await create_token(email)
            if not isinstance(token, str):
                return False, jsonify({"error": "생성된 토큰이 문자열이 아닙니다."}), 500
            
            # 회원가입 한 유저의 id 값 가져오기 
            await session.refresh(new_user)  # refresh to get the UserID
            id = new_user.UserID

            # 신규 토큰 DB 삽입
            success, created, status_code = await new_insert_token(id, token)
    
            if not success:
                return success, created, status_code

            #고객 정보 및 생성된 토큰 반환
            return True, jsonify({
                "email" : new_user.UserEmail,
                "name" : new_user.UserNm,
                "access_token" : token
            }), 201
        
        except Exception as e:
            await session.rollback()  # 트랜잭션 롤백
            return False, jsonify({"error": "사용자 생성 중 오류가 발생했습니다0.", "details": str(e)}), 500
    
async def login_validation(email, pwd):

    user_info = await get_email(email)
    if user_info is None:
        return False, jsonify({"error": "존재하지 않는 이메일입니다."}), 401

    # 패스워드 검증
    success, response, status_code = await verify_password(user_info, pwd)

    if not success:
        return success, response, status_code


    try:
        token_info = await get_token_info(email)
        issued_time = datetime.now() + timedelta(hours=9)
        
    
        # 발행된 토큰이 없거나 만료 되었을 경우 신규 토큰 생성
        if not token_info or token_info.ExpiryAt < issued_time:
        
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

        # 토큰 갱신 (만료 시간이 30분 이하로 남은 경우)
        if token_info.ExpiryAt - issued_time <= timedelta(minutes=30):
            token = await verify_token(email)
            return True, jsonify({
                "email": email, 
                "name": user_info.UserNm,
                "access_token": token
            }), 200
    
        return True, jsonify({
            "email": email, 
            "name": user_info.UserNm,
            "access_token": token_info.AccessToken
        }), 200
    
    except Exception as e:
        return False, jsonify({"error": "사용자 생성 중 오류가 발생했습니다.", "details": str(e)}), 500
