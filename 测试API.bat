@echo off
echo ========================================
echo 测试植物识别API服务
echo ========================================

echo 测试根路径...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/' -UseBasicParsing; Write-Host '✓ 根路径测试成功:' $response.StatusCode; Write-Host $response.Content } catch { Write-Host '✗ 根路径测试失败:' $_.Exception.Message }"

echo.
echo 测试健康检查...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/health' -UseBasicParsing; Write-Host '✓ 健康检查成功:' $response.StatusCode; Write-Host $response.Content } catch { Write-Host '✗ 健康检查失败:' $_.Exception.Message }"

echo.
echo 测试API文档...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/docs' -UseBasicParsing; Write-Host '✓ API文档可访问:' $response.StatusCode } catch { Write-Host '✗ API文档访问失败:' $_.Exception.Message }"

echo.
echo ========================================
echo API服务测试完成
echo ========================================
echo.
echo 如果测试成功，您可以访问：
echo - API服务: http://localhost:8000
echo - API文档: http://localhost:8000/docs
echo - 健康检查: http://localhost:8000/health
echo.
pause 