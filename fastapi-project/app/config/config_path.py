from pathlib import Path


UPLOAD_PATH = Path("/data/mengxf/mysite/upload")
RESULT_PATH = Path("/data/mengxf/mysite/result")

# 确保目录存在
UPLOAD_PATH.mkdir(exist_ok=True, parents=True)
RESULT_PATH.mkdir(exist_ok=True, parents=True)
