import asyncio
import pymysql
from pathlib import Path


async def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='your_database',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


async def check_bcl_complete(task_number: str) -> bool:
    bcl_dir = Path("path/to/bcl") / task_number
    return (bcl_dir / "complete").exists()


async def process_workflow():
    while True:
        try:
            conn = await get_db_connection()
            with conn.cursor() as cursor:
                # 查询未完成的任务
                cursor.execute("""
                    SELECT * FROM tasks
                    WHERE bcl_status = 0
                    AND fastq_status = 0
                    AND analysis_status = 0
                """)
                tasks = cursor.fetchall()

                for task in tasks:
                    if await check_bcl_complete(task['task_number']):
                        # 更新状态
                        cursor.execute("""
                            UPDATE tasks
                            SET bcl_status = 1
                            WHERE task_number = %s
                        """, (task['task_number'],))
                        conn.commit()
                        print(f"任务 {task['task_number']} BCL完成，开始处理...")
                        # TODO: 启动 FASTQ 转换等后续流程

            conn.close()
        except Exception as e:
            print(f"发生错误: {e}")

        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(process_workflow())
