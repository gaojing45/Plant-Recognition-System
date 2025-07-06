@echo off
chcp 65001 >nul
echo ========================================
echo 植物识别系统 - Docker部署脚本
echo ========================================
echo.

:: 检查Docker是否安装
echo [1/6] 检查Docker环境...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker未安装或未启动，请先安装Docker Desktop
    echo 下载地址: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo ✅ Docker已安装

:: 检查Docker Compose
echo [2/6] 检查Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose未安装
    pause
    exit /b 1
)
echo ✅ Docker Compose已安装

:: 创建必要目录
echo [3/6] 创建必要目录...
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
if not exist "data" mkdir data
if not exist "nginx\ssl" mkdir nginx\ssl
echo ✅ 目录创建完成

:: 构建镜像
echo [4/6] 构建Docker镜像...
echo 正在构建镜像，请稍候...
docker-compose -f docker-compose.simple.yml build
if errorlevel 1 (
    echo ❌ 镜像构建失败
    pause
    exit /b 1
)
echo ✅ 镜像构建完成

:: 启动服务
echo [5/6] 启动服务...
docker-compose -f docker-compose.simple.yml up -d
if errorlevel 1 (
    echo ❌ 服务启动失败
    pause
    exit /b 1
)
echo ✅ 服务启动完成

:: 等待服务启动
echo [6/6] 等待服务启动...
timeout /t 10 /nobreak >nul

:: 检查服务状态
echo.
echo ========================================
echo 服务状态检查
echo ========================================
docker-compose -f docker-compose.simple.yml ps

echo.
echo ========================================
echo 部署完成！
echo ========================================
echo 🌐 Web界面: http://localhost:5000
echo 📚 API文档: http://localhost:8000/docs
echo 🔍 API健康检查: http://localhost:8000/health
echo.
echo 常用命令:
echo   查看日志: docker-compose -f docker-compose.simple.yml logs
echo   停止服务: docker-compose -f docker-compose.simple.yml down
echo   重启服务: docker-compose -f docker-compose.simple.yml restart
echo   查看状态: docker-compose -f docker-compose.simple.yml ps
echo.
pause 