##########################################################
############ async test api code : post & get ############
##########################################################

from quart import Blueprint, request, jsonify
from app.models.model import A, async_session, init_models
from sqlalchemy.future import select
import asyncio

t_bp = Blueprint('t', __name__)

data1 = {"name": "John Doe"}

@t_bp.route('/create1/', methods=['POST'])
async def create_person1():
    req = await request.get_json()
    async with async_session() as session:
        session.add(A(name=data1['name']))
        await asyncio.sleep(8)
        await session.commit()
    return 'created'

data2 = {"name": "Jane Smith"}

@t_bp.route('/create2/', methods=['POST'])
async def create_person2():
    req = await request.get_json()
    async with async_session() as session:
        session.add(A(name=data2['name']))
        await asyncio.sleep(5)
        await session.commit()
    return 'created'

data3 = {"name": "Jane Smith"}

@t_bp.route('/create3/', methods=['POST'])
async def create_person3():
    req = await request.get_json()
    async with async_session() as session:
        session.add(A(name=data3['name']))
        await asyncio.sleep(2)
        await session.commit()
    return 'created'

data4 = {"name": "Oba Drake"}

@t_bp.route('/create4/', methods=['POST'])
async def create_person4():
    req = await request.get_json()
    async with async_session() as session:
        session.add(A(name=data4['name']))
        await asyncio.sleep(5)
        await session.commit()
    return 'created'


@t_bp.route('/getData/<name>', methods=['GET'])
async def persons_get(name):
    async with async_session() as session:
        query = await session.execute(select(A).where(A.name == name))
        result = query.scalar()

    return jsonify({"id": result.id, "name": result.name})