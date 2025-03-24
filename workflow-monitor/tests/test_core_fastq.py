import pytest
from src.workflow_monitor.core.core_fastq import is_bcl_conversion_successful


workdir = "/data/mengxf/mysite/results/tasks/20250321_lvis_AHH2WMAFX7"


@pytest.mark.asyncio
async def test_is_bcl_conversion_successful():
    samplesheet = f"{workdir}/samplesheet.csv"
    fastq_res_dir = f"{workdir}/FASTQ"

    assert await is_bcl_conversion_successful(samplesheet, fastq_res_dir)
