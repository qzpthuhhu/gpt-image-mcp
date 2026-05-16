import os
import uuid
from pathlib import Path
from typing import Optional
import httpx
from datetime import datetime

async def download_image(
    url: str,
    output_dir: str,
    filename: Optional[str] = None,
) -> str:
    """下载图片到本地，返回本地路径"""
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 生成文件名
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_part = uuid.uuid4().hex[:6]
        filename = f"gpt-image-{timestamp}-{random_part}.png"

    filepath = Path(output_dir) / filename

    # 下载图片
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            async for chunk in response.aiter_bytes():
                f.write(chunk)

    return str(filepath)