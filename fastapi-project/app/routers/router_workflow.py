from fastapi import APIRouter, HTTPException, UploadFile, Form, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from app.models import model_database
from app.models.model_tasks import TasksResponse, Tasks
from app.config.config_path import RESULT_PATH

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


@router.post("/api/ngs/workflow", response_model=TasksResponse)
async def create_item(
        chipNumber: str = Form(...),
        workflow: str = Form(...),
        samplesheet: UploadFile = File(...),
        session: AsyncSession = Depends(model_database.get_session)
):
    try:
        # 任务编号
        task_number = f"{datetime.now().strftime('%Y%m%d')}_{
            workflow}_{chipNumber}"
        # 检查 工作流+芯片号 是否创建过
        stmt = select(Tasks).where(
            Tasks.workflow == workflow,
            Tasks.chip_number == chipNumber
        ).with_for_update()  # 添加行级锁
        result = await session.execute(stmt)
        item = result.scalar()
        if item:
            await session.rollback()
            raise HTTPException(status_code=400, detail="任务已存在")
        # 工作目录
        work_dir = RESULT_PATH / "tasks" / task_number
        work_dir.mkdir(exist_ok=True, parents=True)
        # 保存 samplesheet
        file_content = await samplesheet.read()
        with open(f"{work_dir}/samplesheet.csv", "wb") as f:
            f.write(file_content)
        # 创建新的任务
        tasks_data = {
            "task_number": task_number,
            "chip_number": chipNumber,
            "workflow": workflow,
            "created_at": datetime.now(),
            "completed_at": None,
            "bcl_status": 0,
            "fastq_status": 0,
            "analysis_status": 0
        }
        new_task = Tasks(**tasks_data)
        session.add(new_task)
        # 明确提交事务
        await session.commit()
        # 刷新获取新数据
        await session.refresh(new_task)
        return new_task
    except Exception as e:
        await session.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")
