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


@router.put("/api/ngs/tasks/{mid}", response_model=TasksResponse)
async def update_task(mid: int, session: AsyncSession = Depends(model_database.get_session)):
    try:
        # 查询任务
        stmt = select(Tasks).where(Tasks.id == mid)
        result = await session.execute(stmt)
        db_task = result.scalar_one_or_none()
        if not db_task:
            raise HTTPException(status_code=404, detail="任务不存在")
        # 更改 bcl, fastq, analysis 状态为 0
        db_task.bcl_status = 0
        db_task.fastq_status = 0
        db_task.analysis_status = 0
        await session.commit()
        await session.refresh(db_task)
        return db_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新任务失败: {str(e)}")


@router.delete("/api/ngs/tasks/{mid}", response_model=TasksResponse)
async def delete_task(mid: int, session: AsyncSession = Depends(model_database.get_session)):
    try:
        # 查询任务
        stmt = select(Tasks).where(Tasks.id == mid)
        result = await session.execute(stmt)
        db_task = result.scalar_one_or_none()
        if not db_task:
            raise HTTPException(status_code=404, detail="任务不存在")
        # 删除任务
        await session.delete(db_task)
        await session.commit()
        return db_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除任务失败: {str(e)}")
