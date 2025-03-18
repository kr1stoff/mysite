from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 配置账号、密码、数据库名
from app.config.config_database import DATABASE_URL

# 创建 SQLAlchemy Base 类
Base = declarative_base()

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    """获取数据库连接"""
    async with async_session() as session:
        yield session
