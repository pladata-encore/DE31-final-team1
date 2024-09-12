from quart import jsonify
from app.models.model import *
from sqlalchemy.future import select

# 데이터 베이스 세션 함수화
async def get_session():
    async with async_session() as session:
        yield session

async def get_ds_list(email): # already checked token
    async with get_session() as session:
        uid = await session.execute(select(UserInfo.UserID).where(UserInfo.UserEmail == email))
        result = await session.execute(select(DsInfo.DsId, DsInfo.DsNm, DsInfo.IsObdc, DsInfo.CreatedAt, DsInfo.UseYn).where(DsInfo.UserID == uid))
        ds_list = result.scalars().all()
        return ds_list

async def create_ds(email, ds_id, ds_name, ds_type): # already checked token
    async with get_session() as session:
        uid = await session.execute(select(UserInfo.UserID).where(UserInfo.UserEmail == email))
        colnm = uid+ds_name
        stmt = DsInfo.insert().values(UserID=uid, DsId=ds_id, DsNm=ds_name, IsObdc=ds_type, DsColNm=colnm, CreatedAt=datetime.now(), UpdatedAt=datetime.now(), UseYn='Y', DelYn='N')
        await session.execute(stmt)
        if(ds_type == 'obdc'):
            create_ds_obdc()
        elif(ds_type == 'ep'):
            create_ds_ep()
        return "OK_CREATED_DS"

# sub function for createds
async def create_ds_ep():
    # CODE_TO_CREATE_DS
    # MAKE SUBPROCESS FOR COLLECT STREAM DATA
    return "OK_CREATED_DS"

async def create_ds_obdc():
    # CODE_TO_CREATE_DS
    # CALL AIRFLOW API TO MAKE DAG
    return "OK_CREATED_DS"
# end of sub function for createds


async def get_ds_info(email, ds_id): # already checked token
    async with get_session() as session:
        uid = await session.execute(select(UserInfo.UserID).where(UserInfo.UserEmail == email))
        stmt = DsInfo.select().where(DsInfo.UserID == uid, DsInfo.DsId == ds_id)
        result = await session.execute(stmt)
        ds_info = result.scalars().all()
        return ds_info

async def get_ds_data(email, ds_id): # already checked token
    #  get actual data from mongoDB
    # ADD CODE LATER
    return "OK_GET_DS_DATA"