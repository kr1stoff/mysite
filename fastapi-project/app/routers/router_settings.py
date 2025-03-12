from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from pathlib import Path

from app.models import model_settings, model_database
from app.models.model_settings import SettingsResponse, SettingsUpdate

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


@router.get("/api/settings", response_model=List[SettingsResponse])
async def read_items(skip: int = 0, limit: int = 100,
                     session: AsyncSession = Depends(model_database.get_session)):
    query = select(model_settings.Settings).offset(skip).limit(limit)
    result = await session.execute(query)
    items = result.scalars().all()
    return items


@router.post("/api/settings", response_model=List[SettingsResponse])
async def update_item(settings_data: SettingsUpdate,
                      session: AsyncSession = Depends(model_database.get_session)):
    # 检查有没有这个路径
    if not Path(settings_data.arg_value).is_dir():
        raise HTTPException(status_code=404, detail="路径不存在")
    try:
        # 更新数据库中的设置
        query = update(model_settings.Settings).\
            where(model_settings.Settings.arg_name == settings_data.arg_name).\
            values(arg_value=settings_data.arg_value)
        await session.execute(query)
        await session.commit()
        # 返回更新后的设置
        result = await session.execute(select(model_settings.Settings))
        items = result.scalars().all()
        return items
    except Exception as e:
        # 如果发生异常,回滚数据库事务
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
