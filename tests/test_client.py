import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

@pytest.mark.asyncio
async def test_generate_image_success():
    """测试成功调用图像生成 API"""
    mock_response_data = {
        "data": [{
            "url": "https://cdn.openai.com/test.png",
            "revised_prompt": "A cute otter"
        }],
        "usage": {"total_tokens": 100}
    }

    # Create a mock response object - json() should return data directly (not a coroutine)
    mock_response = MagicMock()
    mock_response.json = MagicMock(return_value=mock_response_data)
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()

    # Create a mock client with proper async context manager
    mock_client = MagicMock()
    mock_client.post = AsyncMock(return_value=mock_response)
    mock_client.aclose = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_client):
        from src.client import ImageGenerator
        generator = ImageGenerator(api_key="test-key", base_url="https://api.test.com/v1")
        generator.client = mock_client

        result = await generator.generate("a cute otter")

        assert result["images"][0]["url"] == "https://cdn.openai.com/test.png"
        assert result["images"][0]["revised_prompt"] == "A cute otter"
        assert result["model"] == "gpt-image-2"
        assert result["usage"]["total_tokens"] == 100