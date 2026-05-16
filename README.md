# GPT Image MCP Server

MCP Server 封装 GPT Image API，使 Agent 能通过 MCP 协议调用图像生成功能。

## 安装

```bash
cd gpt-image-mcp
pip install -e .
```

## 配置

### 方式 1：配置文件

创建 `~/.gpt-image-mcp.json`：

```json
{
  "api_key": "your-api-key",
  "base_url": "https://api.apiyi.com/v1",
  "output_dir": "~/gpt-images",
  "default_model": "gpt-image-2",
  "default_size": "1024x1024"
}
```

### 方式 2：环境变量

```bash
export GPT_IMAGE_API_KEY=your-api-key
export GPT_IMAGE_OUTPUT_DIR=~/gpt-images
```

## 启动

```bash
python -m src.server
# 或
mcp run src.server
```

## 使用

在 Claude Code 或其他 MCP 客户端中调用 `generate_image` 工具：

```json
{
  "prompt": "A cute baby sea otter floating on its back",
  "model": "gpt-image-2",
  "size": "1024x1024"
}
```

## 开发

```bash
# 安装依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 运行集成测试（需要真实 API Key）
GPT_IMAGE_API_KEY=your-key pytest tests/test_integration.py -v -s
```

## 架构

- `src/config.py` - 配置加载
- `src/client.py` - API 客户端
- `src/downloader.py` - 图片下载器
- `src/server.py` - MCP Server