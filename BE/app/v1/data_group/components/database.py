from quart import jsonify
from app.models.model import *
from sqlalchemy.future import select

# 데이터 베이스 세션 함수화
async def get_session():
    async with async_session() as session:
        yield session

async def get_dg_list(email): # already checked token
    async with get_session() as session:
        uid = await session.execute(select(UserInfo.UserID).where(UserInfo.UserEmail == email))
        result = await session.execute(select(DgInfo.DgId, DgInfo.DgNm, DgInfo.CreatedAt, DgInfo.UseYn).where(DgInfo.UserID == uid))
        dg_list = result.scalars().all()
        return dg_list

async def create_dg(email, dg_id, dg_name, ds_list): # already checked token
    async with get_session() as session:
        uid = await session.execute(select(UserInfo.UserID).where(UserInfo.UserEmail == email))
        stmt = DgInfo.insert().values(UserID=uid, DgId=dg_id, DgNm=dg_name, DsList=ds_list, CreatedAt=datetime.now(), UpdatedAt=datetime.now(), UseYn='Y', DelYn='N')
        await session.execute(stmt)
        return "OK_CREATED_DG"

async def get_dg_info(email, dg_id): # already checked token
    async with get_session() as session:
        uid = await session.execute(select(UserInfo.UserID).where(UserInfo.UserEmail == email))
        stmt = DgInfo.select().where(DgInfo.UserID == uid, DgInfo.DgId == dg_id)
        result = await session.execute(stmt)
        dg_info = result.scalars().all()
        return dg_info

async def get_dg_data(email, dg_id): # already checked token
    async with get_session() as session:
        #  get actual data from mongoDB
        # ADD CODE LATER
        return "OK_GET_DS_DATA"