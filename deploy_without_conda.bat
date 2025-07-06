@echo off
echo 正在部署植物识别项目（不使用conda）...

REM 设置Python路径
set PYTHON_PATH=E:\python\python.exe
set PIP_PATH=E:\python\Scripts\pip.exe

REM 检查Python是否安装
"%PYTHON_PATH%" --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请检查路径 E:\python\python.exe
    echo 请确保Python已正确安装在 E:\python\ 目录下
    pause
    exit /b 1
)

echo Python已安装，版本：
"%PYTHON_PATH%" --version

REM 创建虚拟环境
echo 正在创建虚拟环境...
"%PYTHON_PATH%" -m venv plantid_env

REM 激活虚拟环境
echo 正在激活虚拟环境...
call plantid_env\Scripts\activate.bat

REM 升级pip
echo 正在升级pip...
python -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/

REM 安装依赖（使用国内镜像源）
echo 正在安装项目依赖（使用阿里云镜像源）...
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

echo.
echo 部署完成！
echo 使用方法：
echo 1. 激活环境：plantid_env\Scripts\activate.bat
echo 2. 运行演示：python demo.py
echo 3. 退出环境：deactivate
echo.
pause 