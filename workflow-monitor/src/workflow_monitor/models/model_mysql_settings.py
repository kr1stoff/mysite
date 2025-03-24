from workflow_monitor.models.model_mysql import get_db_connection


async def get_illumina_bcl_dir() -> str:
    """获取 illumina 的 bcl 目录"""
    conn = await get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT arg_value FROM settings
                WHERE arg_name = 'illumina_bcl_directory'
            """)
            return cursor.fetchone()['arg_value']
    finally:
        conn.close()
