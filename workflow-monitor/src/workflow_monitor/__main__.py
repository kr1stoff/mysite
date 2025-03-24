import logging
import asyncio
from workflow_monitor.core.core_monitor import monitor


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    asyncio.run(monitor())
