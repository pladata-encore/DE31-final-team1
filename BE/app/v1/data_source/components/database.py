from quart import jsonify
from app.models.model import *
from sqlalchemy.future import select

async def get_ds_list(email): # already checked token
    async with get_session() as session:
        stmt = '' # CODE_TO_GET_DS_LIST_BY_USER_EMAIL
        result = await session.execute(stmt)
        ds_list = result.scalars().all()
        return ds_list

async def get_ds_info(email, ds_id): # already checked token
    async with get_session() as session:
        stmt = '' # CODE_TO_GET_DS_INFO_BY_DS_ID
        result = await session.execute(stmt)
        ds_info = result.scalars().first()
        return ds_info

async def get_ds_data(email, ds_id): # already checked token
    async with get_session() as session:
        stmt = '' # CODE_TO_GET_DS_DATA_BY_DS_ID, from mongoDB
        result = await session.execute(stmt)
        ds_data = result.scalars().all()
        return ds_data