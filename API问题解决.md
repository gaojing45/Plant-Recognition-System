# API启动问题诊断和解决方案

## 问题描述
用户无法启动植物识别API服务，需要诊断并解决问题。

## 问题分析

### 1. 原始问题
- `api_service.py` 中的 `slowapi` 限流装饰器缺少必需的 `request` 参数
- 错误信息：`No "request" or "websocket" argument on function`

### 2. 依赖问题
- 某些依赖模块可能缺失或版本不兼容
- 虚拟环境激活可能有问题

## 解决方案

### 方案1：修复原始API服务（推荐）

1. **修复限流装饰器问题**
   - 在 `api_service.py` 中的识别函数添加 `request: Request` 参数
   - 添加 `Request` 导入

2. **启动修复后的服务**
   ```bash
   plantid_env\Scripts\activate.bat
   python api_service.py
   ```

### 方案2：使用简化API服务（备用）

1. **创建简化版本**
   - 移除有问题的 `slowapi` 限流功能
   - 保留核心植物识别功能
   - 文件：`simple_api.py`

2. **启动简化服务**
   ```bash
   启动简化API.bat
   ```

## 验证方法

### 1. 检查服务状态
```bash
# 检查端口占用
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

# 检查Python进程
Get-Process python -ErrorAction SilentlyContinue
```

### 2. 测试API端点
```bash
# 测试根路径
Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing

# 测试健康检查
Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing

# 测试API文档
Invoke-WebRequest -Uri "http://localhost:8000/docs" -UseBasicParsing
```

### 3. 使用测试脚本
```bash
python 测试API连接.py
# 或
测试API.bat
```

## 成功标志

API服务成功启动的标志：
- 控制台显示："植物识别器初始化成功"
- 端口8000被占用
- 健康检查返回 `{"status":"healthy"}`
- API文档页面可访问

## 访问地址

- **API服务**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **测试端点**: http://localhost:8000/test

## 故障排除

### 1. 端口被占用
```bash
# 查找占用端口的进程
Get-NetTCPConnection -LocalPort 8000

# 终止进程
Stop-Process -Id <进程ID> -Force
```

### 2. 虚拟环境问题
```bash
# 重新创建虚拟环境
python -m venv plantid_env_new
plantid_env_new\Scripts\activate.bat
pip install -r requirements.txt
```

### 3. 依赖缺失
```bash
# 安装缺失的依赖
pip install fastapi uvicorn slowapi pydantic requests
```

## 下一步

1. 选择方案1或方案2启动API服务
2. 验证服务正常运行
3. 测试植物识别功能
4. 根据需要进一步优化和扩展功能 