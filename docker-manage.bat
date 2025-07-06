@echo off
chcp 65001 >nul
:menu
cls
echo ========================================
echo 植物识别系统 - Docker管理工具
echo ========================================
echo.
echo 请选择操作:
echo.
echo [1] 启动服务
echo [2] 停止服务
echo [3] 重启服务
echo [4] 查看状态
echo [5] 查看日志
echo [6] 重新构建镜像
echo [7] 清理资源
echo [8] 进入容器
echo [9] 备份数据
echo [0] 退出
echo.
set /p choice=请输入选项 (0-9): 

if "%choice%"=="1" goto start
if "%choice%"=="2" goto stop
if "%choice%"=="3" goto restart
if "%choice%"=="4" goto status
if "%choice%"=="5" goto logs
if "%choice%"=="6" goto rebuild
if "%choice%"=="7" goto cleanup
if "%choice%"=="8" goto shell
if "%choice%"=="9" goto backup
if "%choice%"=="0" goto exit
goto menu

:start
echo.
echo 正在启动服务...
docker-compose -f docker-compose.simple.yml up -d
echo ✅ 服务启动完成
pause
goto menu

:stop
echo.
echo 正在停止服务...
docker-compose -f docker-compose.simple.yml down
echo ✅ 服务停止完成
pause
goto menu

:restart
echo.
echo 正在重启服务...
docker-compose -f docker-compose.simple.yml restart
echo ✅ 服务重启完成
pause
goto menu

:status
echo.
echo 服务状态:
docker-compose -f docker-compose.simple.yml ps
echo.
echo 容器资源使用情况:
docker stats --no-stream
pause
goto menu

:logs
echo.
echo 请选择查看哪个服务的日志:
echo [1] API服务日志
echo [2] Web服务日志
echo [3] 所有服务日志
echo [4] 返回主菜单
echo.
set /p log_choice=请输入选项 (1-4): 

if "%log_choice%"=="1" (
    echo API服务日志:
    docker-compose -f docker-compose.simple.yml logs plantid-api
)
if "%log_choice%"=="2" (
    echo Web服务日志:
    docker-compose -f docker-compose.simple.yml logs plantid-web
)
if "%log_choice%"=="3" (
    echo 所有服务日志:
    docker-compose -f docker-compose.simple.yml logs
)
if "%log_choice%"=="4" goto menu
pause
goto menu

:rebuild
echo.
echo 正在重新构建镜像...
docker-compose -f docker-compose.simple.yml build --no-cache
echo ✅ 镜像重新构建完成
echo 是否启动服务? (y/n)
set /p start_after_rebuild=
if /i "%start_after_rebuild%"=="y" (
    docker-compose -f docker-compose.simple.yml up -d
    echo ✅ 服务启动完成
)
pause
goto menu

:cleanup
echo.
echo 正在清理Docker资源...
echo 停止所有容器...
docker-compose -f docker-compose.simple.yml down
echo 删除未使用的镜像...
docker image prune -f
echo 删除未使用的容器...
docker container prune -f
echo 删除未使用的网络...
docker network prune -f
echo 删除未使用的卷...
docker volume prune -f
echo ✅ 清理完成
pause
goto menu

:shell
echo.
echo 请选择要进入的容器:
echo [1] API服务容器
echo [2] Web服务容器
echo [3] 返回主菜单
echo.
set /p shell_choice=请输入选项 (1-3): 

if "%shell_choice%"=="1" (
    echo 进入API服务容器...
    docker-compose -f docker-compose.simple.yml exec plantid-api /bin/bash
)
if "%shell_choice%"=="2" (
    echo 进入Web服务容器...
    docker-compose -f docker-compose.simple.yml exec plantid-web /bin/bash
)
if "%shell_choice%"=="3" goto menu
pause
goto menu

:backup
echo.
echo 正在备份数据...
set backup_dir=backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set backup_dir=%backup_dir: =0%
if not exist "backups" mkdir backups
if not exist "backups\%backup_dir%" mkdir "backups\%backup_dir%"

echo 备份上传文件...
if exist "uploads" xcopy "uploads" "backups\%backup_dir%\uploads\" /E /I /Y >nul

echo 备份日志文件...
if exist "logs" xcopy "logs" "backups\%backup_dir%\logs\" /E /I /Y >nul

echo 备份数据文件...
if exist "data" xcopy "data" "backups\%backup_dir%\data\" /E /I /Y >nul

echo 备份配置文件...
copy "*.yml" "backups\%backup_dir%\" >nul
copy "*.py" "backups\%backup_dir%\" >nul
copy "requirements*.txt" "backups\%backup_dir%\" >nul

echo ✅ 备份完成: backups\%backup_dir%
pause
goto menu

:exit
echo.
echo 感谢使用植物识别系统Docker管理工具！
echo.
exit /b 0 