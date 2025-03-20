from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List


from app.models import model_database
from app.models.model_tasks import TasksResponse, Tasks

router = APIRouter()


@router.on_event("startup")
async def startup():
    # 创建数据库引擎并建立连接
    await model_database.engine.connect()
    # 创建所有定义的数据表
    async with model_database.engine.begin() as conn:
        await conn.run_sync(model_database.Base.metadata.create_all)


@router.on_event("shutdown")
async def shutdown():
    await model_database.engine.dispose()


@router.get("/api/ngs/tasks", response_model=List[TasksResponse])
async def get_tasks(session: AsyncSession = Depends(model_database.get_session)):
    try:
        stmt = select(Tasks).order_by(Tasks.created_at.desc())
        result = await session.execute(stmt)
        tasks = result.scalars().all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务列表失败: {str(e)}")
