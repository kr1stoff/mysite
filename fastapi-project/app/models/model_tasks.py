from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 配置账号、密码、数据库名
from app.config.config_database import DATABASE_URL


# 创建数据库引擎实例
engine = create_engine(DATABASE_URL)

# 创建会话工厂，用于管理数据库会话
# autocommit=False: 不自动提交事务
# autoflush=False: 不自动刷新session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建声明性基类，所有ORM模型类都将继承这个基类
Base = declarative_base()


class Tasks(Base):
    """任务数据表"""
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    # 任务编号. 创建时间+工作流+芯片号
    task_number = Column(String(255), unique=True, index=True)
    chip_number = Column(String(255))
    workflow = Column(String(255))
    created_at = Column(DateTime)
    completed_at = Column(DateTime)
    bcl_status = Column(Integer)
    fastq_status = Column(Integer)
    analysis_status = Column(Integer)


class TasksResponse(BaseModel):
    """任务响应模型"""
    id: int
    task_number: str
    chip_number: str
    workflow: str
    created_at: datetime
    # completed_at: datetime
    completed_at: Optional[datetime] = None  # 允许为 None
    bcl_status: int
    fastq_status: int
    analysis_status: int

    class Config:
        from_attributes = True


class TasksCreate(BaseModel):
    """任务创建模型"""
    tasks_number: str
    chip_number: str
    workflow: str
    created_at: datetime
    completed_at: datetime
    bcl_status: int
    fastq_status: int
    analysis_status: int
