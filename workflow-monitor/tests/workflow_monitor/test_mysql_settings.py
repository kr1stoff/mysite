import pytest
from workflow_monitor.models.model_mysql_settings import get_illumina_bcl_dir


@pytest.mark.asyncio
async def test_get_illumina_bcl_dir():
    dir = await get_illumina_bcl_dir()
    print(dir)
