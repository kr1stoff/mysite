import asyncio
import logging

from workflow_monitor.config.config import SLEEP_TIME
from workflow_monitor.core.core_bcl import bcl
from workflow_monitor.core.core_fastq import fastq


async def monitor():
    while True:
        try:
            # 监测 BCL 生成
            await bcl()
            # BCL 转 FASTQ 流程
            await fastq()
        except Exception as e:
            logging.error("发生错误: ", e)

        # ! 等待一段时间检查一下
        await asyncio.sleep(SLEEP_TIME)
