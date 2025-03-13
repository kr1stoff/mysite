from pathlib import Path


UPLOAD_PATH = Path("/data/mengxf/mysite/uploads")
RESULT_PATH = Path("/data/mengxf/mysite/results")

# 确保目录存在
UPLOAD_PATH.mkdir(exist_ok=True, parents=True)
RESULT_PATH.mkdir(exist_ok=True, parents=True)
