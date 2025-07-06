# 🐳 植物识别系统 - Docker部署指南

## 📋 目录
- [系统要求](#系统要求)
- [快速开始](#快速开始)
- [详细部署步骤](#详细部署步骤)
- [配置说明](#配置说明)
- [管理命令](#管理命令)
- [故障排除](#故障排除)
- [高级配置](#高级配置)

## 🖥️ 系统要求

### 最低要求
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Docker**: Docker Desktop 4.0+ 或 Docker Engine 20.10+
- **Docker Compose**: 2.0+
- **内存**: 4GB RAM
- **存储**: 10GB 可用空间
- **网络**: 稳定的互联网连接

### 推荐配置
- **操作系统**: Windows 11, macOS 12+, Ubuntu 20.04+
- **Docker**: Docker Desktop 4.15+ 或 Docker Engine 23.0+
- **内存**: 8GB RAM
- **存储**: 20GB 可用空间
- **CPU**: 4核心以上

## 🚀 快速开始

### 1. 一键部署（推荐）
```bash
# Windows
docker-deploy.bat

# Linux/macOS
chmod +x docker-deploy.sh
./docker-deploy.sh
```

### 2. 手动部署
```bash
# 构建并启动服务
docker-compose -f docker-compose.simple.yml up -d

# 查看服务状态
docker-compose -f docker-compose.simple.yml ps
```

## 📝 详细部署步骤

### 步骤1: 安装Docker
1. **Windows/macOS**: 下载并安装 [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. **Ubuntu**: 
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose
   sudo usermod -aG docker $USER
   ```

### 步骤2: 克隆项目
```bash
git clone <项目地址>
cd quarrying-plant-id
```

### 步骤3: 检查环境
```bash
# 检查Docker版本
docker --version
docker-compose --version

# 检查Docker服务状态
docker info
```

### 步骤4: 部署服务
```bash
# 使用简化配置（推荐）
docker-compose -f docker-compose.simple.yml up -d

# 或使用完整配置（包含监控）
docker-compose up -d
```

### 步骤5: 验证部署
```bash
# 检查服务状态
docker-compose -f docker-compose.simple.yml ps

# 查看日志
docker-compose -f docker-compose.simple.yml logs
```

## ⚙️ 配置说明

### 端口配置
| 服务 | 端口 | 说明 |
|------|------|------|
| Web界面 | 5000 | 用户友好的Web界面 |
| API服务 | 8000 | RESTful API接口 |
| API文档 | 8000/docs | Swagger UI文档 |
| Nginx | 80 | 反向代理（可选） |
| Redis | 6379 | 缓存服务（可选） |
| Prometheus | 9090 | 监控服务（可选） |
| Grafana | 3000 | 监控面板（可选） |

### 环境变量
```bash
# 在docker-compose.yml中配置
environment:
  - PYTHONPATH=/app
  - PYTHONUNBUFFERED=1
  - LOG_LEVEL=INFO
  - MAX_UPLOAD_SIZE=16M
```

### 数据卷映射
```yaml
volumes:
  - ./logs:/app/logs          # 日志文件
  - ./uploads:/app/uploads    # 上传文件
  - ./data:/app/data          # 数据文件
  - ./plantid/models:/app/plantid/models:ro  # 模型文件（只读）
```

## 🛠️ 管理命令

### 使用管理脚本
```bash
# Windows
docker-manage.bat

# 功能包括：
# - 启动/停止/重启服务
# - 查看状态和日志
# - 重新构建镜像
# - 清理资源
# - 备份数据
```

### 常用Docker命令
```bash
# 服务管理
docker-compose -f docker-compose.simple.yml up -d      # 启动服务
docker-compose -f docker-compose.simple.yml down       # 停止服务
docker-compose -f docker-compose.simple.yml restart    # 重启服务

# 查看状态
docker-compose -f docker-compose.simple.yml ps         # 服务状态
docker-compose -f docker-compose.simple.yml logs       # 查看日志
docker stats                                           # 资源使用情况

# 镜像管理
docker-compose -f docker-compose.simple.yml build      # 构建镜像
docker-compose -f docker-compose.simple.yml build --no-cache  # 重新构建

# 容器管理
docker-compose -f docker-compose.simple.yml exec plantid-api bash  # 进入容器
docker system prune -a                               # 清理所有未使用资源
```

## 🔧 故障排除

### 常见问题

#### 1. 端口被占用
```bash
# 检查端口占用
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/macOS

# 修改端口映射
# 在docker-compose.yml中修改ports配置
ports:
  - "8001:8000"  # 将主机端口改为8001
```

#### 2. 内存不足
```bash
# 增加Docker内存限制
# Docker Desktop -> Settings -> Resources -> Memory

# 或使用轻量级配置
docker-compose -f docker-compose.simple.yml up -d
```

#### 3. 模型文件加载失败
```bash
# 检查模型文件是否存在
ls -la plantid/models/

# 重新下载模型文件
python tools/download_models.py
```

#### 4. 服务启动失败
```bash
# 查看详细日志
docker-compose -f docker-compose.simple.yml logs plantid-api

# 检查容器状态
docker-compose -f docker-compose.simple.yml ps

# 重新构建镜像
docker-compose -f docker-compose.simple.yml build --no-cache
```

### 日志分析
```bash
# 实时查看日志
docker-compose -f docker-compose.simple.yml logs -f

# 查看特定服务的日志
docker-compose -f docker-compose.simple.yml logs plantid-api

# 查看最近的日志
docker-compose -f docker-compose.simple.yml logs --tail=100
```

## 🚀 高级配置

### 生产环境部署

#### 1. 使用优化版Dockerfile
```bash
# 构建优化镜像
docker build -f Dockerfile.optimized -t plantid:optimized .

# 使用优化镜像
docker-compose -f docker-compose.prod.yml up -d
```

#### 2. 配置Nginx反向代理
```bash
# 启用Nginx服务
docker-compose up -d nginx

# 访问地址
# http://localhost (通过Nginx)
# http://localhost/api/ (API服务)
# http://localhost/docs (API文档)
```

#### 3. 配置SSL证书
```bash
# 生成自签名证书
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/nginx.key \
  -out nginx/ssl/nginx.crt

# 启用HTTPS
# 取消nginx.conf中HTTPS部分的注释
```

#### 4. 配置监控
```bash
# 启动完整监控栈
docker-compose up -d prometheus grafana

# 访问监控面板
# http://localhost:3000 (Grafana)
# 用户名: admin
# 密码: admin123
```

### 性能优化

#### 1. 资源限制
```yaml
# 在docker-compose.yml中添加
services:
  plantid-api:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

#### 2. 缓存配置
```yaml
# 启用Redis缓存
services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
```

#### 3. 负载均衡
```yaml
# 多实例部署
services:
  plantid-api:
    deploy:
      replicas: 3
    ports:
      - "8000-8002:8000"
```

## 📊 监控和维护

### 健康检查
```bash
# API健康检查
curl http://localhost:8000/health

# 容器健康状态
docker-compose -f docker-compose.simple.yml ps
```

### 数据备份
```bash
# 自动备份
docker-manage.bat  # 选择备份选项

# 手动备份
docker run --rm -v plantid_uploads:/data -v $(pwd)/backup:/backup alpine tar czf /backup/uploads.tar.gz -C /data .
```

### 日志管理
```bash
# 日志轮转
# 在docker-compose.yml中配置
services:
  plantid-api:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 🔐 安全建议

### 1. 网络安全
- 使用防火墙限制端口访问
- 配置SSL/TLS加密
- 定期更新Docker镜像

### 2. 容器安全
- 使用非root用户运行容器
- 限制容器权限
- 扫描镜像漏洞

### 3. 数据安全
- 定期备份重要数据
- 加密敏感配置
- 监控异常访问

## 📞 技术支持

### 获取帮助
1. 查看日志文件: `logs/`
2. 检查服务状态: `docker-compose ps`
3. 查看文档: `README.md`
4. 提交Issue: [项目地址]/issues

### 联系信息
- 项目维护者: [维护者信息]
- 技术支持: [支持邮箱]
- 文档地址: [文档链接]

---

**注意**: 本部署指南适用于植物识别系统v1.0及以上版本。如有问题，请参考故障排除部分或联系技术支持。 