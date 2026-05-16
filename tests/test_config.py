import os
import json
import tempfile
from pathlib import Path

def test_load_config_from_file():
    """测试从配置文件加载配置"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / ".gpt-image-mcp.json"
        config_path.write_text(json.dumps({
            "api_key": "test-key-123",
            "output_dir": "~/test-images",
            "default_model": "gpt-image-2",
            "default_size": "1024x1024"
        }))

        os.environ["GPT_IMAGE_CONFIG_PATH"] = str(config_path)

        from src.config import load_config
        config = load_config()

        assert config["api_key"] == "test-key-123"
        assert config["default_model"] == "gpt-image-2"
        # output_dir 应该展开 ~
        assert config["output_dir"].startswith("/")

def test_env_var_override():
    """测试环境变量覆盖配置文件"""
    os.environ["GPT_IMAGE_API_KEY"] = "env-key-456"
    os.environ["GPT_IMAGE_OUTPUT_DIR"] = "/tmp/test"

    from src.config import load_config
    config = load_config()

    assert config["api_key"] == "env-key-456"
    assert config["output_dir"] == "/tmp/test"