from pathlib import Path


async def check_bcl_complete(task_number: str) -> bool:
    bcl_dir = Path("path/to/bcl") / task_number
    return (bcl_dir / "complete").exists()
