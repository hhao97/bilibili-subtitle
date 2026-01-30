FROM python:3.10-slim

# (可选) 一些包编译依赖。没有需要可删掉 build-essential
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# 用 uv 根据 pyproject.toml + uv.lock 安装依赖到系统环境
RUN pip install --no-cache-dir uv \
    && uv sync --system --frozen

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["python", "-m", "uvicorn", "bilibili_video_info_mcp.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
