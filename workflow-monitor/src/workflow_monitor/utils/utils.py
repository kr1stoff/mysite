from pathlib import Path
from subprocess import run

from workflow_monitor.config.config_path import RESULT_PATH



async def create_logdir(task_number: str) -> Path:
    """
    创建 log 目录
    :param task_number: 任务编号
    :return:
    """
    logdir = RESULT_PATH.joinpath(f"tasks/{task_number}/logs").resolve()
    logdir.mkdir(parents=True, exist_ok=True)
    return logdir



async def myrun(cmd: str, logfile: str):
    """
    异步执行系统命令并将输出写入日志文件

    :param cmd: 要执行的系统命令
    :param logfile: 日志文件路径，命令输出将写入此文件
    :return: None
    """
    res = run(cmd, shell=True, capture_output=True, text=True)
    with open(logfile, "w") as f:
        f.write(f"CMD: {cmd}\n")
        f.write("[STDOUT]\n")
        f.write(res.stdout)
        f.write("[STDERR]\n")
        f.write(res.stderr)
