import pytest
from src.workflow_monitor.models.model_mysql_tasks import get_latest_bcl_task, get_lastest_fastq_task


@pytest.mark.asyncio
async def test_get_latest_bcl_task():
    task = await get_latest_bcl_task()
    print(task)


@pytest.mark.asyncio
async def test_get_lastest_fastq_task():
    task = await get_lastest_fastq_task()
    print(task)
