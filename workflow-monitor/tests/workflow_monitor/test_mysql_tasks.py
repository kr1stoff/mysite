import pytest
from workflow_monitor.models.model_mysql_tasks import get_latest_task


@pytest.mark.asyncio
async def test_get_latest_task():
    task = await get_latest_task()
    print(task)
