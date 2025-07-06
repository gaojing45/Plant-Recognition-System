#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import hashlib
import json
from datetime import datetime
from typing import List, Optional

import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import uvicorn

# 导入植物识别模块
try:
    import plantid
    PLANTID_AVAILABLE = True
except ImportError as e:
    print(f"植物识别模块导入失败: {e}")
    PLANTID_AVAILABLE = False

if not PLANTID_AVAILABLE:
    print("植物识别模块不可用，无法启动API服务")
    exit(1)

# 创建FastAPI应用
app = FastAPI(
    title="植物识别API服务",
    description="基于AI的植物识别API，支持4,066种植物分类",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 安全认证
security = HTTPBearer()

# 全局变量
plant_identifier = None
api_keys = {
    "demo_key": "demo_user",
    "test_key": "test_user"
}

# 缓存
cache = {}
cache_ttl = 3600  # 1小时

# 数据模型
class IdentificationResult(BaseModel):
    chinese_name: str
    latin_name: str
    probability: float
    rank: int

class IdentificationResponse(BaseModel):
    status: str
    message: str
    results: List[IdentificationResult]
    process_time: float
    timestamp: str
    image_hash: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str
    uptime: float
    model_loaded: bool

def get_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """验证API密钥"""
    token = credentials.credentials
    if token not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的API密钥",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return api_keys[token]

def init_plant_identifier():
    """初始化植物识别器"""
    global plant_identifier
    if plant_identifier is None:
        try:
            plant_identifier = plantid.PlantIdentifier()
            print("植物识别器初始化成功")
            return True
        except Exception as e:
            print(f"植物识别器初始化失败: {e}")
            return False
    return True

def get_image_hash(image_data: bytes) -> str:
    """计算图片哈希值用于缓存"""
    return hashlib.md5(image_data).hexdigest()

def check_cache(image_hash: str) -> Optional[dict]:
    """检查缓存"""
    if image_hash in cache:
        cached_data = cache[image_hash]
        if time.time() - cached_data['timestamp'] < cache_ttl:
            return cached_data['data']
    return None

def set_cache(image_hash: str, data: dict):
    """设置缓存"""
    cache[image_hash] = {
        'data': data,
        'timestamp': time.time()
    }
    # 清理过期缓存
    current_time = time.time()
    expired_keys = [k for k, v in cache.items() if current_time - v['timestamp'] > cache_ttl]
    for key in expired_keys:
        del cache[key]

def validate_image_file(file: UploadFile) -> bool:
    """验证图片文件"""
    if file.filename is None:
        return False
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    file_extension = os.path.splitext(file.filename)[1].lower()
    return file_extension in allowed_extensions

def process_image(file: UploadFile, topk: int = 5) -> dict:
    """处理图片识别"""
    start_time = time.time()
    
    # 读取图片
    file_content = file.file.read()
    nparr = np.frombuffer(file_content, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise HTTPException(status_code=400, detail="无法读取图片文件")
    
    # 检查缓存
    image_hash = get_image_hash(file_content)
    cached_result = check_cache(image_hash)
    if cached_result:
        cached_result['from_cache'] = True
        return cached_result
    
    # 进行识别
    if not init_plant_identifier():
        raise HTTPException(status_code=500, detail="植物识别器初始化失败")
    
    outputs = plant_identifier.identify(image, topk=topk)
    process_time = time.time() - start_time
    
    if outputs['status'] != 0:
        raise HTTPException(status_code=500, detail=outputs['message'])
    
    # 格式化结果
    results = []
    for i, result in enumerate(outputs['results']):
        results.append(IdentificationResult(
            chinese_name=result['chinese_name'],
            latin_name=result['latin_name'],
            probability=result['probability'],
            rank=i + 1
        ))
    
    response_data = {
        'status': 'success',
        'message': '识别成功',
        'results': results,
        'process_time': round(process_time, 3),
        'timestamp': datetime.now().isoformat(),
        'image_hash': image_hash,
        'from_cache': False
    }
    
    # 设置缓存
    set_cache(image_hash, response_data)
    
    return response_data

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    print("正在启动植物识别API服务...")
    if init_plant_identifier():
        print("植物识别器初始化成功")
    else:
        print("警告：植物识别器初始化失败")

@app.get("/", response_model=dict)
async def root():
    """根路径"""
    return {
        "message": "植物识别API服务",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.post("/identify", response_model=IdentificationResponse)
async def identify_plant(
    file: UploadFile = File(...),
    topk: int = 5,
    api_key: str = Depends(get_api_key)
):
    """
    单张图片植物识别
    
    - **file**: 图片文件
    - **topk**: 返回结果数量 (1-20)
    - **api_key**: API密钥
    """
    if not validate_image_file(file):
        raise HTTPException(status_code=400, detail="不支持的文件格式")
    
    try:
        result = process_image(file, topk)
        return IdentificationResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    uptime = time.time() - getattr(app, 'start_time', time.time())
    
    return HealthResponse(
        status='healthy' if init_plant_identifier() else 'unhealthy',
        message='服务正常运行' if init_plant_identifier() else '植物识别器未初始化',
        timestamp=datetime.now().isoformat(),
        uptime=round(uptime, 2),
        model_loaded=plant_identifier is not None
    )

@app.get("/test")
async def test_endpoint():
    """测试端点"""
    return {
        "message": "API服务正常运行",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": plant_identifier is not None
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """通用异常处理器"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "内部服务器错误",
            "message": str(exc),
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )

if __name__ == "__main__":
    app.start_time = time.time()
    print("植物识别API服务启动中...")
    print("访问地址: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000) 