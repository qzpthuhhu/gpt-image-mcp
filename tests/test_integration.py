import os
import pytest

@pytest.mark.skipif(
    not os.environ.get("GPT_IMAGE_API_KEY"),
    reason="Requires GPT_IMAGE_API_KEY env var"
)
async def test_end_to_end():
    """端到端测试：生成图片并下载到本地"""
    from src.config import load_config
    from src.client import ImageGenerator
    from src.downloader import download_image
    import tempfile

    config = load_config()

    # 生成图片
    generator = ImageGenerator(api_key=config["api_key"], base_url=config["base_url"])
    try:
        result = await generator.generate(prompt="a cute sea otter")
        assert len(result["images"]) > 0

        # 下载到本地
        img = result["images"][0]
        if img.get("url"):
            local_path = await download_image(
                url=img["url"],
                output_dir=config["output_dir"],
            )
            from pathlib import Path
            assert Path(local_path).exists()
    finally:
        await generator.close()