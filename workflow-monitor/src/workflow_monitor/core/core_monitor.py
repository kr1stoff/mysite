import asyncio
import logging

from workflow_monitor.config.config_time import SLEEP_TIME


async def monitor():
    while True:
        try:
            pass
        except Exception as e:
            logging.error("发生错误: ", e)

        # ! 等待一段时间检查一下
        await asyncio.sleep(SLEEP_TIME)
