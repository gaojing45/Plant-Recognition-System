@echo off
echo ========================================
echo 植物识别项目手动部署脚本
echo Python路径: E:\python\python.exe
echo ========================================

REM 设置Python路径
set PYTHON_PATH=E:\python\python.exe

echo 步骤1: 检查Python安装...
"%PYTHON_PATH%" --version
if errorlevel 1 (
    echo 错误：Python未找到，请检查 E:\python\python.exe 是否存在
    pause
    exit /b 1
)

echo.
echo 步骤2: 创建虚拟环境...
"%PYTHON_PATH%" -m venv plantid_env
if errorlevel 1 (
    echo 错误：创建虚拟环境失败
    pause
    exit /b 1
)

echo.
echo 步骤3: 激活虚拟环境...
call plantid_env\Scripts\activate.bat
if errorlevel 1 (
    echo 错误：激活虚拟环境失败
    pause
    exit /b 1
)

echo.
echo 步骤4: 升级pip（使用阿里云镜像源）...
python -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
if errorlevel 1 (
    echo 警告：pip升级失败，继续安装依赖...
)

echo.
echo 步骤5: 安装项目依赖（使用阿里云镜像源）...
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
if errorlevel 1 (
    echo 错误：依赖安装失败
    echo 尝试使用其他镜像源...
    pip install -r requirements.txt -i https://pypi.douban.com/simple/
    if errorlevel 1 (
        echo 错误：所有镜像源都失败，请检查网络连接
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo 部署成功！
echo ========================================
echo 使用方法：
echo 1. 激活环境：plantid_env\Scripts\activate.bat
echo 2. 运行演示：python demo.py
echo 3. 退出环境：deactivate
echo.
echo 或者直接运行：run_demo.bat
echo ========================================
pause 