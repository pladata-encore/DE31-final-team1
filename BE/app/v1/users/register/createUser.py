from quart import Blueprint, request, jsonify
from app.models.model import UserInfo, async_session
from sqlalchemy.future import select
import base64
import bcrypt # type: ignore 


# Create Blueprint
createUser_bp = Blueprint('createUser',__name__)

# Create Users
@createUser_bp.route('/createUser/', methods=['POST', 'OPTIONS'])
async def createUser():
    async with async_session() as session:
        if request.method == 'OPTIONS':
            # 프리플라이트 요청 처리
            return jsonify({"message": "Preflight request"}), 200

        # requests 정보 매핑
        req = await request.get_json()

        # JSON 데이터 유효성 검사
        if req is None:
            return jsonify({"error": "요청에 잘못된 또는 누락된 JSON이 있습니다."}), 400
        
        name = req.get("name")
        email = req.get("email")
        pwd = req.get("password")

        # 1. 필수 정보 체크
        if not name or not email or not pwd:
            return jsonify({"error": "이름, 이메일, 패스워드는 필수 항목입니다."})
        
        # 테이블 정보를 search에 할당하여 유저명 검색결과 result에 매핑
        search = await session.execute(select(UserInfo).where(UserInfo.UserEmail == email))
        result = search.scalar()

        # 2. 입력한 이메일이 중복일 경우 체크
        if result is not None:
            return jsonify({"error": "중복된 이메일입니다."}), 400

        # 디코딩 & 해시화 (64글자)
        # client에서 base64로 인코딩 된 값을 디코딩 -> 해시화 -> 문자열로 변환
        decoded_pwd = base64.b64encode(pwd.encode("utf-8"))
        hashed_pwd = bcrypt.hashpw(decoded_pwd, bcrypt.gensalt())
        serializable_pwd = hashed_pwd.decode("utf-8")

        # 신규 유저 정보 매핑 
        new_user = UserInfo(UserNm=name, UserEmail=email, UserPwd=hashed_pwd)

        try:
            if result != email:
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