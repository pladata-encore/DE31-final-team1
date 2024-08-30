from quart import jsonify
from app.models.model import *
from sqlalchemy.future import select

async def check_token(email, token):
    # function to check if the token is valid
    # get token from db by email
    async with get_session() as session:
        stmt = '' # CODE_TO_GET_TOKEN_FROM_DB
        result = await session.execute(stmt)

        # if token is not in db, return false
        if result is None:
            return "ERR_NO_TOKEN"

        token, exp_time = result.scalars().first()

        # if token is expired, return false
        if exp_time < datetime.now():
            return "ERR_EXPIRED_TOKEN"
        
        # if token is not matched, return false
        if token != token:
            return "ERR_NOT_MATCHED_TOKEN"

        # if expired time is less than 30 min, update exp_time and return true
        if exp_time - datetime.now() < timedelta(minutes=30):
            stmt = '' # CODE_TO_UPDATE_EXPIRE_TIME
            await session.execute(stmt)
            return "OK_UPDATED_EXPIRE_TIME"
        
        # else return true
        return "OK_VALID_TOKEN"

async def update_token(email, name, pwd):
    # function to update token, when login
    async with get_session() as session:
        stmt = '' # CODE_TO_UPDATE_TOKEN, and get token
        result = await session.execute(stmt)

        token = result.scalars().first()

        if token is None:
            return "ERR_MAKING_TOKEN"

        # else
        return "OK_UPDATED_TOKEN", token