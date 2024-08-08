from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config.settings import DATABASE_URL

# 데이터베이스 엔진 및 세션 설정
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

# 테이블 정의
class A(Base):
    __tablename__ = 'test_table'
    id = Column(Integer, primary_key=True)
    name = Column(String(20)) 

class UserInfo(Base):
    __tablename__ = 'UserInfo'
    UserId = Column(String(20), primary_key=True)
    UserNm = Column(String(50))
    UserEmail = Column(String(30))
    UserPwd = Column(String(64))

# 초기화
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# async def reset_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)