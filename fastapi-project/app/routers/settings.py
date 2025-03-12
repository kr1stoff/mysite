from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models import settings, database
from app.models.settings import SettingsResponse

router = APIRouter()


@router.on_event("startup")
async def startup():
    # 创建数据库引擎并建立连接
    await database.engine.connect()
    # 创建所有定义的数据表
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)


@router.on_event("shutdown")
async def shutdown():
    await database.engine.dispose()


@router.get("/api/settings", response_model=List[SettingsResponse])
async def readd_items(skip: int = 0,
                      limit: int = 100,
                      session: AsyncSession = Depends(database.get_session)):
    result = await session.execute(select(settings.Settings).offset(skip).limit(limit))
    items = result.scalars().all()
    print(items)
    return items
