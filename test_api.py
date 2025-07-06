#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "植物识别API测试服务"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "服务正常运行"}

if __name__ == "__main__":
    print("正在启动测试API服务...")
    print("访问地址: http://localhost:8000")
    print("健康检查: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000) 