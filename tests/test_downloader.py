import tempfile
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

async def test_download_image_success():
    """测试成功下载图片到本地"""
    image_data = b"fake_image_data"

    with tempfile.TemporaryDirectory() as tmpdir:
        async def mock_get(url):
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()

            # Create an async iterator for aiter_bytes
            async def async_byte_iterator():
                yield image_data

            mock_response.aiter_bytes = MagicMock(return_value=async_byte_iterator())
            return mock_response

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = mock_get
            mock_client.__aenter__.return_value = mock_client
            mock_client_class.return_value = mock_client

            from src.downloader import download_image
            result = await download_image(
                url="https://cdn.openai.com/test.png",
                output_dir=tmpdir,
                filename="test-image.png"
            )

            assert Path(result).exists()
            assert Path(result).read_bytes() == image_data