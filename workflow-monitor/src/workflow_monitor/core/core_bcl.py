import logging
from pathlib import Path
import asyncio

from workflow_monitor.models.model_mysql_tasks import get_latest_bcl_task, update_task_status
from workflow_monitor.models.model_mysql_settings import get_illumina_bcl_dir
from workflow_monitor.config.config import SLEEP_TIME


async def bcl():
    """检查 BCL 生成状态"""
    task = await get_latest_bcl_task()
    if not task:
        logging.info("没有未完成的 BCL 任务")
        await asyncio.sleep(SLEEP_TIME)
        return

    logging.info(f"当前 BCL 任务信息: {task}")
    tid = task["id"]
    chip_number = task["chip_number"]

    # 检查 BCL 生成状态
    bcldir = await get_illumina_bcl_dir()
    curr_bcldir_res = list(Path(bcldir).glob(f'*{chip_number}'))
    # 未开始
    if not curr_bcldir_res:
        logging.info("还未开始测序")
    else:
        curr_bcldir = curr_bcldir_res[0]
        logging.debug(f"当前 BCL 文件夹: {curr_bcldir}")
        rta_complete = Path(curr_bcldir) / "RTAComplete.txt"
        # 正在测序
        if not rta_complete.exists():
            logging.info("正在生成 BCL 文件")
            await update_task_status(tid, "bcl_status", 1)
        # 测序完成
        else:
            logging.info("BCL 文件生成完成")
            await update_task_status(tid, "bcl_status", 2)
