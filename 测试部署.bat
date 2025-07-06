@echo off
echo ========================================
echo 测试植物识别项目部署
echo ========================================

REM 设置Python路径
set PYTHON_PATH=E:\python\python.exe

echo 1. 测试Python安装...
"%PYTHON_PATH%" --version
if errorlevel 1 (
    echo ❌ Python未找到
    pause
    exit /b 1
)
echo ✅ Python安装正常

echo.
echo 2. 测试虚拟环境创建...
"%PYTHON_PATH%" -m venv test_plantid_env
if errorlevel 1 (
    echo ❌ 虚拟环境创建失败
    pause
    exit /b 1
)
echo ✅ 虚拟环境创建成功

echo.
echo 3. 测试虚拟环境激活...
call test_plantid_env\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 虚拟环境激活失败
    pause
    exit /b 1
)
echo ✅ 虚拟环境激活成功

echo.
echo 4. 测试pip安装（使用阿里云镜像）...
pip install opencv-python -i https://mirrors.aliyun.com/pypi/simple/ --quiet
if errorlevel 1 (
    echo ❌ pip安装失败
    echo 尝试使用豆瓣镜像...
    pip install opencv-python -i https://pypi.douban.com/simple/ --quiet
    if errorlevel 1 (
        echo ❌ 所有镜像源都失败
        pause
        exit /b 1
    )
)
echo ✅ pip安装成功

echo.
echo 5. 清理测试环境...
call test_plantid_env\Scripts\deactivate.bat
rmdir /s /q test_plantid_env

echo.
echo ========================================
echo ✅ 所有测试通过！可以开始部署
echo ========================================
echo 请运行：deploy_without_conda.bat
echo ========================================
pause 