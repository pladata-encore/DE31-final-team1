from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Boolean  
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config.settings import DATABASE_URL
from datetime import datetime, timedelta

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
    UserID = Column(Integer, primary_key=True, autoincrement=True)
    UserNm = Column(String(20))
    UserEmail = Column(String(50))
    UserPwd = Column(String(64))

class JwtInfo(Base):
    __tablename__ = 'JwtInfo'
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    UserID = Column(Integer, ForeignKey('UserInfo.UserID'), nullable=True)
    AccessToken = Column(String(1024), nullable=True)
    IssuedAt = Column(DateTime, nullable=True)
    ExpiryAt = Column(DateTime, nullable=True)

class UserPGInfo(Base):
    __tablename__ = 'UserPGInfo'
    PgID = Column(String(50), primary_key=True,nullable=False)
    UserID = Column(Integer, ForeignKey('UserInfo.UserID'),nullable=False)
    PgName = Column(String(50), nullable=True)
    CreatedAt = Column(DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(hours=9))  
    UpdatedAt = Column(DateTime, nullable=True, onupdate=datetime.utcnow) 
    DelYn = Column(Boolean, nullable=True, default=False)
   
    

    

# 초기화
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# async def reset_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)