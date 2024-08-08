from quart import Blueprint, request, jsonify
from app.models.model import A, async_session, init_models
from sqlalchemy.future import select
import asyncio

v2_bp = Blueprint('v2', __name__)

@v2_bp.route('/person', methods=['POST'])
async def person_post():
    pass
    req = await request.get_json()
    # 여기에 버전 2의 로직을 추가
    return 'created in v2', 201