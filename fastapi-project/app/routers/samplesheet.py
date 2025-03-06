from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
import pandas as pd
import csv

from custom import get_path


router = APIRouter()
upldir = Path(get_path()["upload"])


@router.post("/api/ngs/samplesheet")
async def create_samplesheet(file: UploadFile = File(...)):
    """上传文件"""
    crnt_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    crnt_task_upldir = upldir / crnt_time
    crnt_task_upldir.mkdir(parents=True, exist_ok=True)
    # 检查文件类型是否为Excel
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="仅支持 Excel 文件")
    # 保存文件到指定目录
    file_location = f"{crnt_task_upldir}/{file.filename}"
    contents = await file.read()
    with open(file_location, "wb") as buffer:
        buffer.write(contents)

    # 处理文件
    out_smpsht_csv = f"{crnt_task_upldir}/{Path(file_location).stem}-samplesheet.csv"
    create(file_location, out_smpsht_csv)

    # 返回 JSON 响应
    return JSONResponse(content={"message": "文件上传成功", "file": file.filename})


def create(smpsht_excel, out_smpsht_csv):
    # samplesheet 表头
    smpsht_head = """[Header]
    IEMFileVersion,5
    Date,2022/5/26
    Workflow,GenerateFASTQ
    Application,NextSeq FASTQ Only
    Instrument Type,NextSeq/MiniSeq
    Assay,Nextera DNA
    Index Adapters,"Nextera Index Kit (24 Indexes 96 Samples)"
    Chemistry,Amplicon

    [Reads]
    151
    151

    [Settings]

    [Data]
    Sample_ID,Sample_Name,Sample_Plate,Sample_Well,I7_Index_ID,index,I5_Index_ID,index2,Sample_Project,Description
    """
    df = pd.read_excel(smpsht_excel)
    # csv 先写 samplesheet_header，然后迭代df追加写到csv中
    with open(out_smpsht_csv, "w", newline="") as csvfile:
        csvfile.write(smpsht_head)
        for row in df.iterrows():
            outlst = [""] * 10
            outlst[0] = row[1]["Sample_ID"]
            outlst[5] = row[1]["index"]
            outlst[7] = row[1]["index2"]
            csvfile.write(",".join(outlst) + "\n")
