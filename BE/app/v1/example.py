# from quart import Blueprint, request, jsonify
# from app.models.model import A, async_session, init_models
# from sqlalchemy.future import select
# import asyncio

# v1_bp = Blueprint('v1', __name__)

# ####  데이터 삽입  ####
# # 데이터 생성
# @v1_bp.route('/create/', methods=['POST'])
# async def person_post():
#     req = await request.get_json()
#     async with async_session() as session:
#         session.add(A(name=req['name']))
#         await session.commit()
#     return 'created'

# # 부분 업데이트 
# @v1_bp.route('/update/<int:id>', methods=['PUT'])
# async def person_put(id):
#     req = await request.get_json()
#     name = req.get("name")
#     async with async_session() as session:
#         query = await session.excute(select(A).where(id=id))
#         result = query.scalar().first()
#         result.name = name
#         await session.commit()
#     return "Data updated successfully"

# ####  데이터 조회  ####
# # 일괄 조회
# @v1_bp.route('/reads/', methods=['GET'])
# async def person_get():
#     async with async_session() as session:
#         query = await session.execute(select(A))
#         results = query.scalars().all()

#     return jsonify([{"id": result.id, "name": result.name} for result in results])

# # 특정 개인 조회
# @v1_bp.route('/read/<name>', methods=['GET'])
# async def persons_get(name):
#     async with async_session() as session:
#         query = await session.execute(select(A).where(A.name == name))
#         result = query.scalar()

#     return jsonify({"id": result.id, "name": result.name})


# # 서버 시작 시 데이터베이스 초기화
# loop = asyncio.get_event_loop()
# loop.run_until_complete(init_models())
