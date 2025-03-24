import asyncio
import logging

from workflow_monitor.config.config_time import SLEEP_TIME
from workflow_monitor.core.core_bcl import bcl


async def monitor():
    while True:
        try:
            # 监测 BCL 生成
            await bcl()
        except Exception as e:
            logging.error("发生错误: ", e)

        # ! 等待一段时间检查一下
        await asyncio.sleep(SLEEP_TIME)
