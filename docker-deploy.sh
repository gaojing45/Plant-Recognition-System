#!/bin/bash

# 植物识别系统 - Docker部署脚本 (Linux/macOS)
# 使用方法: chmod +x docker-deploy.sh && ./docker-deploy.sh

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_header() {
    echo "========================================"
    print_message $BLUE "植物识别系统 - Docker部署脚本"
    echo "========================================"
    echo
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_message $RED "❌ $1 未安装"
        return 1
    else
        print_message $GREEN "✅ $1 已安装"
        return 0
    fi
}

# 检查Docker环境
check_docker_environment() {
    print_message $YELLOW "[1/6] 检查Docker环境..."
    
    if ! check_command "docker"; then
        print_message $RED "请先安装Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! check_command "docker-compose"; then
        print_message $RED "请先安装Docker Compose: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    # 检查Docker服务状态
    if ! docker info &> /dev/null; then
        print_message $RED "❌ Docker服务未启动，请启动Docker服务"
        exit 1
    fi
    
    print_message $GREEN "✅ Docker服务正常运行"
}

# 创建必要目录
create_directories() {
    print_message $YELLOW "[2/6] 创建必要目录..."
    
    local dirs=("logs" "uploads" "data" "nginx/ssl" "backups")
    
    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            print_message $GREEN "✅ 创建目录: $dir"
        else
            print_message $BLUE "ℹ️  目录已存在: $dir"
        fi
    done
    
    print_message $GREEN "✅ 目录创建完成"
}

# 检查模型文件
check_model_files() {
    print_message $YELLOW "[3/6] 检查模型文件..."
    
    local model_dir="plantid/models"
    local required_files=(
        "quarrying_plantid_model.onnx"
        "quarrying_plantid_label_map.txt"
    )
    
    if [ ! -d "$model_dir" ]; then
        print_message $RED "❌ 模型目录不存在: $model_dir"
        exit 1
    fi
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$model_dir/$file" ]; then
            print_message $RED "❌ 模型文件缺失: $file"
            exit 1
        fi
    done
    
    print_message $GREEN "✅ 模型文件检查完成"
}

# 构建Docker镜像
build_images() {
    print_message $YELLOW "[4/6] 构建Docker镜像..."
    
    print_message $BLUE "正在构建镜像，请稍候..."
    
    if docker-compose -f docker-compose.simple.yml build; then
        print_message $GREEN "✅ 镜像构建完成"
    else
        print_message $RED "❌ 镜像构建失败"
        exit 1
    fi
}

# 启动服务
start_services() {
    print_message $YELLOW "[5/6] 启动服务..."
    
    if docker-compose -f docker-compose.simple.yml up -d; then
        print_message $GREEN "✅ 服务启动完成"
    else
        print_message $RED "❌ 服务启动失败"
        exit 1
    fi
}

# 等待服务启动
wait_for_services() {
    print_message $YELLOW "[6/6] 等待服务启动..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            print_message $GREEN "✅ API服务已就绪"
            break
        fi
        
        print_message $BLUE "等待服务启动... ($attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        print_message $YELLOW "⚠️  服务启动超时，请检查日志"
    fi
}

# 显示服务状态
show_service_status() {
    echo
    echo "========================================"
    print_message $BLUE "服务状态检查"
    echo "========================================"
    
    docker-compose -f docker-compose.simple.yml ps
    
    echo
    echo "========================================"
    print_message $GREEN "部署完成！"
    echo "========================================"
    echo "🌐 Web界面: http://localhost:5000"
    echo "📚 API文档: http://localhost:8000/docs"
    echo "🔍 API健康检查: http://localhost:8000/health"
    echo
    echo "常用命令:"
    echo "  查看日志: docker-compose -f docker-compose.simple.yml logs"
    echo "  停止服务: docker-compose -f docker-compose.simple.yml down"
    echo "  重启服务: docker-compose -f docker-compose.simple.yml restart"
    echo "  查看状态: docker-compose -f docker-compose.simple.yml ps"
    echo
}

# 主函数
main() {
    print_header
    
    check_docker_environment
    create_directories
    check_model_files
    build_images
    start_services
    wait_for_services
    show_service_status
}

# 错误处理
trap 'print_message $RED "部署过程中发生错误，请检查日志"; exit 1' ERR

# 运行主函数
main "$@" 