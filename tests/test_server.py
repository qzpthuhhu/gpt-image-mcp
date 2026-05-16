from unittest.mock import patch, AsyncMock
import pytest

@pytest.mark.asyncio
async def test_generate_image_tool():
    """测试 MCP 工具 generate_image"""
    # Mock config 和 client
    with patch("src.server.load_config") as mock_config, \
         patch("src.server.ImageGenerator") as mock_gen:

        mock_config.return_value = {
            "api_key": "test-key",
            "base_url": "https://api.test.com/v1",
            "output_dir": "/tmp/test",
            "default_model": "gpt-image-2",
            "default_size": "1024x1024",
        }

        mock_generator = AsyncMock()
        mock_generator.generate.return_value = {
            "images": [{"url": "https://test.com/img.png", "revised_prompt": "test"}],
            "model": "gpt-image-2",
        }
        mock_gen.return_value = mock_generator

        from src.server import generate_image_tool

        # 模拟调用
        result = await generate_image_tool(prompt="a cute otter")

        assert result["success"] == True
        assert len(result["images"]) == 1