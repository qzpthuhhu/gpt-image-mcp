# GPT Image MCP Server

MCP Server 封装 GPT Image API，使 Agent 能通过 MCP 协议调用图像生成功能。

## 功能

- 通过 MCP 协议提供 `generate_image` 工具
- 支持 `gpt-image-2` 等模型
- 同时返回图片 URL 和本地保存路径
- 支持配置文件和环境变量配置
- 跨设备使用（API Key 不写入代码）

## 快速开始

### 1. 安装

```bash
git clone https://github.com/qzpthuhhu/gpt-image-mcp.git
cd gpt-image-mcp
pip install -e .
```

### 2. 配置

**方式一：配置文件**（推荐，跨设备使用）

在 `~/.gpt-image-mcp.json` 创建配置文件：

```json
{
  "api_key": "your-api-key",
  "base_url": "https://api.apiyi.com/v1",
  "output_dir": "~/gpt-images",
  "default_model": "gpt-image-2",
  "default_size": "1024x1024"
}
```

**方式二：环境变量**

```bash
export GPT_IMAGE_API_KEY=your-api-key
export GPT_IMAGE_OUTPUT_DIR=~/gpt-images
```

### 3. 在 Claude Code 中配置 MCP Server

在 `~/.claude.json` 的 `mcpServers` 中添加：

```json
{
  "mcpServers": {
    "gpt-image": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/Users/qinzhanpeng/gpt-image-mcp"
    }
  }
}
```

> **注意**：`cwd` 需要修改为你实际的 gpt-image-mcp 目录路径

### 4. 重启 Claude Code

重启后 MCP Server 会自动连接。

## 使用方法

### Agent 调用

Agent 可以直接调用 `generate_image` 工具。

### 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| prompt | string | 是 | — | 图像描述（英文效果最佳） |
| model | string | 否 | gpt-image-2 | 模型名 |
| size | string | 否 | 1024x1024 | 尺寸，支持 1024x1024, 1024x1792, 1792x1024 |
| n | int | 否 | 1 | 生成数量 |
| output_dir | string | 否 | ~/gpt-images | 保存目录 |

### 返回值

```json
{
  "success": true,
  "images": [
    {
      "url": "https://cdn.openai.com/...",
      "local_path": "/Users/xxx/gpt-images/gpt-image-xxx.png",
      "revised_prompt": "A cute dog playing on the beach"
    }
  ],
  "model": "gpt-image-2",
  "total_cost": "0.04"
}
```

## 多设备配置

在不同电脑上使用时：

1. Clone 仓库到本地
2. 安装依赖：`pip install -e .`
3. 创建配置文件 `~/.gpt-image-mcp.json`
4. 在 Claude Code 配置中添加 MCP Server（修改 cwd 为实际路径）
5. 重启 Claude Code

## 手动测试

```bash
cd /path/to/gpt-image-mcp
python -m src.server
```

MCP Server 通过 stdio 通信，Claude Code 会自动处理输入输出。

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 运行集成测试（需要真实 API Key）
GPT_IMAGE_API_KEY=your-key pytest tests/test_integration.py -v -s
```

## 项目结构

```
gpt-image-mcp/
├── src/
│   ├── config.py      # 配置加载
│   ├── client.py       # API 客户端
│   ├── downloader.py   # 图片下载
│   └── server.py       # MCP Server
├── tests/              # 测试
├── pyproject.toml
└── README.md
```

## 安全说明

- API Key 保存在本地配置文件中，不提交到 GitHub
- 配置文件路径：`~/.gpt-image-mcp.json`
- `.env.example` 是模板，不包含真实 API Key