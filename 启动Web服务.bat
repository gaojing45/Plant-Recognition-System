@echo off
echo ========================================
echo 启动植物识别Web服务
echo ========================================

REM 激活虚拟环境
call plantid_env\Scripts\activate.bat

REM 创建必要的目录
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
if not exist "data" mkdir data

echo 正在启动Flask Web服务...
echo 访问地址: http://localhost:5000
echo.
python web_app.py

pause 