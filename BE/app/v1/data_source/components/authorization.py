from quart import jsonify
from app.models.model import *
from sqlalchemy.future import select

# 데이터 베이스 세션 함수화
async def get_session():
    async with async_session() as session:
        yield session

async def check_token(email, token):
    # function to check if the token is valid
    async with get_session() as session:
        # get uid from db by email
        uid = await session.execute(select(UserInfo.UserID).where(UserInfo.UserEmail == email))
        try:
            result = await session.execute(select(JwtInfo.AccessToken, JwtInfo.ExpiryAt).where(JwtInfo.UserID == uid))
        except:
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
            time_to_update = datetime.now() + timedelta(minutes=30)
            stmt = JwtInfo.update().where(JwtInfo.UserID == uid).values(ExpiryAt = time_to_update)
            await session.execute(stmt)
            return "OK_UPDATED_EXPIRE_TIME"
        
        # else return true
        return "OK_VALID_TOKEN"

async def update_token(email, name, pwd):
    # function to update token, when login
    async with get_session() as session:
        stmt = '' # SQL_TO_UPDATE_TOKEN, and get token
        result = await session.execute(stmt)

        token = result.scalars().first()

        if token is None:
            return "ERR_MAKING_TOKEN"

        # else
        return "OK_UPDATED_TOKEN", token