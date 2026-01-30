FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8000
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "uvicorn", "bilibili_video_info_mcp.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
