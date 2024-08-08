from quart import Blueprint, request, jsonify
from app.models.model import A, async_session, init_models
from sqlalchemy.future import select
import asyncio

# Create Blueprint
users_bp = Blueprint('users',__name__)


@users_bp.route('/users/', methods=['POST'])
async def createUser():
    req = await request.get_json()
    async with async_session() as session:
        session.add(A(name=req['name']))
    
        await session.commit()
    return 'created'


@users_bp.route('/reads/', methods=['GET'])
async def person_get():
    async with async_session() as session:
        query = await session.execute(select(A))
        results = query.scalars().all()

    return jsonify([{"id": result.id, "name": result.name} for result in results])