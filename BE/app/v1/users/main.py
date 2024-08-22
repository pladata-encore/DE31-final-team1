from quart import Blueprint
from .components.common import *
from .components.functions import *

main_bp = Blueprint('main',__name__)

@main_bp.route('/createUser/', methods=['POST', 'OPTIONS'])
async def createUser():

        await preflight_request()
        
        # 정합성 체크
        success, req = await json_validation(require_name=True)

        if not success:
            return req
        
        # 유저 생성
        success, created, status_code = await create_user(req.email, req.name, req.pwd)

        if not success:
            return created, status_code
        
        return created, status_code
    

@main_bp.route('/login/', methods=['POST', 'OPTIONS'])
async def login():

        await preflight_request()
        
        # 정합성 체크
        success, req = await json_validation(require_name=False)

        if not success:
            return req
        
        # 로그인
        success, login_token, status_code = await login_validation(req.email, req.pwd)

        if not success:
              return login_token, status_code
        
        return login_token, status_code
        

