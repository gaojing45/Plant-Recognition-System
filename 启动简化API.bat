@echo off
echo ========================================
echo 启动简化植物识别API服务
echo ========================================

REM 激活虚拟环境
call plantid_env\Scripts\activate.bat

REM 创建必要的目录
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
if not exist "data" mkdir data

echo 正在启动简化FastAPI服务...
echo 访问地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo.
python simple_api.py

pause 