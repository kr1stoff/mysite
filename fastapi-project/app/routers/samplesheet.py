from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from custom import get_path
from pathlib import Path
from time import time


router = APIRouter()
upldir = Path(get_path()['upload'])


@router.post("/api/ngs/samplesheet")
async def create_samplesheet(file: UploadFile = File(...)):
    """上传文件"""
    crnt_task_upldir = upldir / str(time()).split('.')[0]  # 时间戳命名
    crnt_task_upldir.mkdir(parents=True, exist_ok=True)
    # 检查文件类型是否为Excel
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="仅支持 Excel 文件")
    # 保存文件到指定目录
    file_location = f"{crnt_task_upldir}/{file.filename}"
    contents = await file.read()
    with open(file_location, "wb") as buffer:
        buffer.write(contents)
    return JSONResponse(content={"message": "文件上传成功", "file": file.filename})


def create():
    pass
