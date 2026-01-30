# Repository Guidelines

## 项目结构与模块组织
- `bilibili_video_info_mcp/`：核心源码。`bilibili_api.py` 负责与 Bilibili API 交互，`server.py` 暴露 MCP 服务，`__init__.py`/`__main__.py` 提供入口。
- `.github/workflows/`：CI 工作流（构建与基础冒烟检查）。
- `README.md`、`README.zh.md`：使用说明与示例。
- `.env.example`：本地配置模板；`Dockerfile` 提供容器化打包。

## 构建、测试与开发命令
- `python -m build`：构建 sdist/wheel（CI 使用此命令）。
- `pip install dist/*.whl`：本地安装构建产物，用于冒烟检查导入。
- `bilibili-video-info-mcp sse` / `bilibili-video-info-mcp streamable-http`：启动服务（需先安装包并准备 `.env`）。
- `uvx run --env .env bilibili-video-info-mcp sse`：使用 uvx 运行示例（见 README）。

## 编码风格与命名约定
- Python 4 空格缩进，遵循 PEP 8；函数与变量使用 `snake_case`，类使用 `PascalCase`。
- 保持模块职责清晰，避免跨文件重复逻辑；优先小函数与清晰参数。
- 变更前先阅读现有实现，保持错误处理与返回结构一致。

## 测试指南
- 当前未配置专门测试框架；CI 仅执行构建与导入冒烟检查。
- 若新增核心逻辑，建议同步引入测试框架并扩展 CI，再更新本指南。

## 提交与 PR 规范
- 提交信息风格接近 `type: summary`（例如 `feat: ...`, `docs: ...`, `ci: ...`, `refactor: ...`），允许中英文混用但需简洁明确。
- PR 需包含：变更动机、影响范围、验证方式（命令或步骤），如涉及接口变更请更新 README 示例。

## 安全与配置提示
- `SESSDATA` 为必要环境变量，勿提交真实值；优先使用 `.env` 并从 `.env.example` 拷贝。
- 涉及网络请求的变更需考虑速率限制与错误回退，避免硬编码敏感信息。
