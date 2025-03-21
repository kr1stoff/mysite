from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
import pandas as pd

from app.config.config_path import RESULT_PATH


router = APIRouter()


@router.post("/api/ngs/samplesheet")
async def create_samplesheet(file: UploadFile = File(...)):
    """上传文件"""
    crnt_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    crnt_task_resdir = RESULT_PATH / "samplesheet" / crnt_time
    crnt_task_resdir.mkdir(parents=True, exist_ok=True)

    # 保存文件到指定目录
    file_location = f"{crnt_task_resdir}/{file.filename}"
    contents = await file.read()
    with open(file_location, "wb") as buffer:
        buffer.write(contents)

    # 检查文件格式和内容
    chk_res = check_input(file_location)
    if chk_res:
        # ! 返回 HTTP 400 错误
        raise HTTPException(status_code=400, detail=chk_res)

    # 处理文件
    out_smpsht_csv = f"{
        crnt_task_resdir}/{Path(file_location).stem}-samplesheet.csv"
    write_samplesheet(file_location, out_smpsht_csv)

    # * 返回 JSON 响应
    return JSONResponse(content={
        "message": "文件处理成功",
        "task_id": crnt_time,
        "filename": Path(out_smpsht_csv).name
    })


def check_input(infile: str):
    """
    检查输入文件
    infile: 输入文件
    return: 错误信息
    """
    # 检查文件类型是否为Excel
    if not infile.endswith((".xls", ".xlsx")):
        return "仅支持 Excel 文件"
    # 打开 Excel 文件，检查
    df = pd.read_excel(infile)
    # 检查文件是否为空
    if len(df) == 0:
        return "文件为空"
    # 检查是否包含必要的列
    required_columns = ["Sample_ID", "index", "index2"]
    if not set(required_columns).issubset(df.columns):
        return "缺少必要的列"
    # 检查是否包含重复的样本ID
    if len(df["Sample_ID"]) != len(df["Sample_ID"].unique()):
        return "存在重复的样本ID"
    # 检查是否包含重复的index组合
    idx_combs = df["index"] + df["index2"]
    if len(idx_combs) != len(idx_combs.unique()):
        return "存在重复的index组合"
    # 都成功的话
    return


def write_samplesheet(smpsht_excel, out_smpsht_csv):
    """
    生成 samplesheet
    smpsht_excel:   samplesheet excel
    out_smpsht_csv: 输出的 samplesheet csv
    """
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
