from quart import jsonify
from app.models.model import *
from sqlalchemy.future import select

async def get_dg_list(email): # already checked token
    async with get_session() as session:
        stmt = '' # CODE_TO_GET_DG_LIST_BY_USER_EMAIL
        result = await session.execute(stmt)
        dg_list = result.scalars().all()
        return dg_list

async def get_dg_info(email, dg_id): # already checked token
    async with get_session() as session:
        stmt = '' # CODE_TO_GET_DG_INFO_BY_DG_ID
        result = await session.execute(stmt)
        dg_info = result.scalars().first()
        return dg_info

async def get_dg_data(email, dg_id): # already checked token
    async with get_session() as session:
        stmt = '' # CODE_TO_GET_DG_DATA_BY_DG_ID, from mongoDB
        result = await session.execute(stmt)
        dg_data = result.scalars().all()
        return dg_data