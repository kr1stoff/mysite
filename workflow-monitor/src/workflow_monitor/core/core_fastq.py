import asyncio
import logging
import csv
from pathlib import Path

from workflow_monitor.config.config import SLEEP_TIME
from workflow_monitor.config.config_path import RESULT_PATH
from workflow_monitor.config.config_conda import CONDA_ACTIVATE, CONDA_ENV_BASIC
from workflow_monitor.models.model_mysql_tasks import get_lastest_fastq_task, update_task_status
from workflow_monitor.models.model_mysql_settings import get_illumina_bcl_dir
from workflow_monitor.utils.utils import create_logdir, myrun


async def fastq():
    """
    BCL 转 FASTQ 流程
    """
    task = await get_lastest_fastq_task()
    if not task:
        logging.info("没有未完成的 BCL 转 FASTQ 任务.")
        await asyncio.sleep(SLEEP_TIME)
        return

    logging.info(f"BCL 转 FASTQ 流程. 当前任务信息: {task}")
    tid = task["id"]
    task_number = task["task_number"]
    chip_number = task["chip_number"]

    # log 目录
    logdir = await create_logdir(task_number)
    logfile = logdir / "bcl2fastq.log"

    # BCL 目录, samplesheet 文件, fastq 输出目录
    ilmn_bcl_dir = await get_illumina_bcl_dir()
    bcldir = list(Path(ilmn_bcl_dir).glob(f'*{chip_number}'))[0]
    fastq_res_dir = f"{RESULT_PATH}/tasks/{task_number}/FASTQ"
    samplesheet = f"{RESULT_PATH}/tasks/{task_number}/samplesheet.csv"

    # 开始 BCL 转 FASTQ 流程
    # 更新 MySQL 任务状态为开始
    logging.info(f"开始 BCL 转 FASTQ 流程.")
    await update_task_status(tid, "fastq_status", 1)
    # 执行 BCL 转 FASTQ 流程
    cml = f"""
source {CONDA_ACTIVATE} {CONDA_ENV_BASIC}
bcl2fastq --no-lane-splitting --barcode-mismatches 1 --processing-threads 32 \
    --runfolder-dir {bcldir} \
    --input-dir {bcldir}/Data/Intensities/BaseCalls \
    --sample-sheet {samplesheet} \
    --output-dir {fastq_res_dir}
"""
    await myrun(cml, logfile)
    if await is_bcl_conversion_successful(samplesheet, fastq_res_dir):
        # 更新 MySQL 任务状态为完成
        logging.info(f"BCL 转 FASTQ 流程完成.")
        await update_task_status(tid, "fastq_status", 2)
    else:
        # 更新 MySQL 任务状态为异常
        logging.error(f"BCL 转 FASTQ 流程异常!")
        await update_task_status(tid, "fastq_status", 3)


async def is_bcl_conversion_successful(samplesheet: str, fastq_res_dir: str):
    """
    检查是否所有样本都拆分成功
    :param samplesheet: samplesheet 文件
    :param fastq_res_dir: fastq 输出目录
    :return: 布尔值
    """
    with open(samplesheet, "r") as f:
        for line in f:
            if line.startswith("[Data]"):
                contents = f.read()
        lines = contents.strip().split("\n")
        reader = csv.DictReader(lines)
        sample_ids = [row["Sample_ID"] for row in reader]

    for sample_id in sample_ids:
        fastq_files = list(Path(fastq_res_dir).glob(f"{sample_id}*.fastq.gz"))
        if not fastq_files:
            return False

    return True
