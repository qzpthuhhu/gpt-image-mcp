from mcp.server import Server
from mcp.types import Tool, TextContent
import asyncio
from datetime import datetime

from .config import load_config
from .client import ImageGenerator
from .downloader import download_image

# MCP Server 实例
server = Server("gpt-image-mcp")

@server.list_tools()
async def list_tools():
    """列出所有可用工具"""
    return [
        Tool(
            name="generate_image",
            description="使用 GPT Image API 生成图片，支持通过 URL 访问或本地保存访问",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "图像描述（英文效果最佳）",
                    },
                    "model": {
                        "type": "string",
                        "description": "模型名",
                        "default": "gpt-image-2",
                    },
                    "size": {
                        "type": "string",
                        "description": "图片尺寸",
                        "default": "1024x1024",
                        "enum": ["1024x1024", "1024x1792", "1792x1024"],
                    },
                    "n": {
                        "type": "integer",
                        "description": "生成数量",
                        "default": 1,
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "本地保存目录",
                    },
                },
                "required": ["prompt"],
            },
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """执行工具调用"""
    if name == "generate_image":
        return await generate_image_tool(**arguments)
    raise ValueError(f"Unknown tool: {name}")

async def generate_image_tool(
    prompt: str,
    model: str = "gpt-image-2",
    size: str = "1024x1024",
    n: int = 1,
    output_dir: str = None,
) -> dict:
    """生成图片的核心逻辑"""
    config = load_config()

    # 使用参数或默认值
    if output_dir is None:
        output_dir = config["output_dir"]

    api_key = config["api_key"]
    base_url = config["base_url"]

    # 调用 API
    generator = ImageGenerator(api_key=api_key, base_url=base_url)
    try:
        result = await generator.generate(
            prompt=prompt,
            model=model,
            size=size,
            n=n,
        )
    finally:
        await generator.close()

    # 下载图片到本地
    images = []
    for img in result["images"]:
        local_path = None
        if img.get("url"):
            try:
                local_path = await download_image(
                    url=img["url"],
                    output_dir=output_dir,
                )
            except Exception:
                pass  # 下载失败不影响返回 URL
        elif img.get("b64_json"):
            try:
                local_path = await download_image(
                    b64_json=img["b64_json"],
                    output_dir=output_dir,
                )
            except Exception:
                pass

        images.append({
            "url": img.get("url"),
            "local_path": local_path,
            "revised_prompt": img.get("revised_prompt"),
        })

    return {
        "success": True,
        "images": images,
        "model": result.get("model", model),
        "total_cost": str(result.get("usage", {}).get("total_tokens", "N/A")),
    }

def main():
    """启动 MCP Server"""
    import mcp.server.stdio
    async def run_server():
        server = Server("gpt-image-mcp")
        init_options = server.create_initialization_options()
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, init_options)
    asyncio.run(run_server())

if __name__ == "__main__":
    main()