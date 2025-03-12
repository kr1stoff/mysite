from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# 配置账号、密码、数据库名
from app.config import DATABASE_URL


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Settings(Base):
    """设置页面数据表"""
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    arg_name = Column(String(255), unique=True, index=True)
    arg_value = Column(String(255), index=True)


class SettingsResponse(BaseModel):
    """创建 Pydantic 响应模型"""
    arg_name: str
    arg_value: str

    class Config:
        from_attributes = True


class SettingsUpdate(BaseModel):
    """创建 Pydantic 更新模型"""
    arg_name: str
    arg_value: str
