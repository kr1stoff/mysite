from pathlib import Path
import yaml


def get_path():
    """获取路径"""
    home = Path(__file__).parents[1]
    # 路径字典
    return yaml.safe_load(home.joinpath('config/path.yaml').read_text(encoding='utf-8'))
