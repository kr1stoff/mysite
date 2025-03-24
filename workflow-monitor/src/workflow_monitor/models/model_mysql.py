import pymysql

from workflow_monitor.config.config_mysql import MySQL_CONFIG


async def get_db_connection():
    return pymysql.connect(**MySQL_CONFIG)
