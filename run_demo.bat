@echo off
echo 正在启动植物识别演示...

REM 激活虚拟环境
call plantid_env\Scripts\activate.bat

REM 运行演示
python demo.py

REM 退出环境
deactivate
pause 