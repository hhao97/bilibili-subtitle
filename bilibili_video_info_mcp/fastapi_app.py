import os
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from . import bilibili_api

load_dotenv()

app = FastAPI(title="Bilibili Video Info API")


class VideoInfoRequest(BaseModel):
    url: str
    sessdata: str | None = Field(default=None, alias="SESSDATA")

    class Config:
        allow_population_by_field_name = True


class VideoInfoResponse(BaseModel):
    subtitles: List[Dict[str, Any]]
    danmaku: List[str]
    comments: List[Dict[str, Any]]


@app.post("/video-info", response_model=VideoInfoResponse)
async def get_video_info(payload: VideoInfoRequest) -> VideoInfoResponse:
    url = payload.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="url 不能为空")
    sessdata = payload.sessdata
    if not sessdata and not os.getenv("SESSDATA"):
        raise HTTPException(status_code=400, detail="SESSDATA 缺失，请在请求体提供 SESSDATA 或设置环境变量")

    bvid = bilibili_api.extract_bvid(url)
    if not bvid:
        raise HTTPException(status_code=400, detail=f"无法从 URL 提取 BV 号: {url}")

    aid, cid, error = bilibili_api.get_video_basic_info(bvid, sessdata=sessdata)
    if error:
        raise HTTPException(status_code=502, detail=f"获取视频信息失败: {error.get('error')}")

    subtitles, error = bilibili_api.get_subtitles(aid, cid, sessdata=sessdata)
    if error:
        raise HTTPException(status_code=502, detail=f"获取字幕失败: {error.get('error')}")

    danmaku, error = bilibili_api.get_danmaku(cid, sessdata=sessdata)
    if error:
        raise HTTPException(status_code=502, detail=f"获取弹幕失败: {error.get('error')}")

    comments, error = bilibili_api.get_comments(aid, sessdata=sessdata)
    if error:
        raise HTTPException(status_code=502, detail=f"获取评论失败: {error.get('error')}")

    return VideoInfoResponse(
        subtitles=subtitles or [],
        danmaku=danmaku or [],
        comments=comments or [],
    )

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/")
def root():
    return {"ok": True}
