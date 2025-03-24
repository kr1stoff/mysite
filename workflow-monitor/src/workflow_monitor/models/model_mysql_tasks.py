from typing import Dict, Optional

from workflow_monitor.models.model_mysql import get_db_connection


async def get_latest_bcl_task() -> Optional[Dict]:
    """
    获取最近的 BCL 任务信息, 这一步与脚本运行无关, 只是单纯监测BCL生成状态
    bcl_status: 0-未开始, 1-正在生成, 2-生成完成
    :return: 任务信息字典, 或 None
    """
    conn = await get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM tasks
                WHERE bcl_status IN (0, 1)
                ORDER BY id DESC
                LIMIT 1
            """)
            return cursor.fetchone()
    finally:
        conn.close()


async def update_task_status(task_id: int, column: str, status: int):
    """
    更新任务状态
    :param task_id: 任务ID
    :param column: 要更新的列名, bcl_status, fastq_status, analysis_status
    :param status: 新的状态值, 仅允许 0-3 之间的整数
    """
    if status not in [0, 1, 2, 3]:
        raise ValueError("状态值必须在 0-3 之间")
    if column not in ["bcl_status", "fastq_status", "analysis_status"]:
        raise ValueError("列名必须是 bcl_status, fastq_status 或 analysis_status")
    conn = await get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = f"""
                UPDATE tasks
                SET {column} = %s
                WHERE id = %s
            """
            cursor.execute(sql, (status, task_id))
        conn.commit()
    finally:
        conn.close()
