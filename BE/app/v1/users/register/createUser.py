from quart import Blueprint, request, jsonify
from app.models.model import UserInfo, async_session
from sqlalchemy.future import select
import base64
import bcrypt # type: ignore


# Create Blueprint
createUser_bp = Blueprint('createUser',__name__)

# Create Users
@createUser_bp.route('/createUser/', methods=['POST'])
async def createUser():
    async with async_session() as session:
           
        # requests 정보 매핑
        req = await request.get_json()
        id = req.get("id")
        name = req.get("name")
        email = req.get("email")
        pwd = req.get("password")

        # 1. 필수 정보 체크
        if not name or not email or not pwd:
            return jsonify({"error": "이름, 이메일, 패스워드는 필수 항목입니다."})
        
        # 테이블 정보를 search에 할당하여 유저명 검색결과 result에 매핑
        search = await session.execute(select(UserInfo).where(UserInfo.UserNm == name))
        result = search.scalar()

        # 2. 입력한 이름이 중복일 경우 체크
        if result == name:
            return jsonify({"error": "중복된 이름입니다."})

        # 디코딩 & 해시화 (64글자)
        decoded_pwd = base64.b64encode(pwd.encode()).decode()
        hashed_pwd = bcrypt.hashpw(decoded_pwd.encode(), bcrypt.gensalt())
        serializable_pwd = hashed_pwd.decode("utf-8")
        # 신규 유저 정보 매핑
        new_user = UserInfo(UserId=id, UserNm=name, UserEmail=email, UserPwd=hashed_pwd)

        try:
            # 3. 중복이 없을 경우 DB에 추가
            session.add(new_user)
            await session.commit()
            return jsonify({"response": 200, 
                            "message" : "Successfully", 
                            "user" : {
                                "name" : new_user.UserNm,
                                "email" : new_user.UserEmail,
                                "pwd" : serializable_pwd
                            }})
        except Exception as e:
            return jsonify({"error": str(e)})