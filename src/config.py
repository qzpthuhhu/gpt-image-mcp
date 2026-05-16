import os
import json
from pathlib import Path

DEFAULT_CONFIG = {
    "api_key": "",
    "base_url": "https://api.apiyi.com/v1",
    "output_dir": "~/Downloads/gpt-images",
    "default_model": "gpt-image-2",
    "default_size": "1024x1024",
}

def load_config() -> dict:
    """加载配置，优先级：环境变量 > 配置文件 > 默认值"""
    config = DEFAULT_CONFIG.copy()

    # 1. 从配置文件加载
    config_path = os.environ.get(
        "GPT_IMAGE_CONFIG_PATH",
        str(Path.home() / ".gpt-image-mcp.json")
    )
    if os.path.exists(config_path):
        with open(config_path) as f:
            file_config = json.load(f)
            config.update(file_config)

    # 2. 环境变量覆盖
    for key in ["api_key", "base_url", "output_dir", "default_model", "default_size"]:
        env_key = f"GPT_IMAGE_{key.upper()}"
        if env_key in os.environ:
            config[key] = os.environ[env_key]

    # 3. 展开 ~ 为实际 home 目录
    config["output_dir"] = os.path.expanduser(config["output_dir"])

    return config