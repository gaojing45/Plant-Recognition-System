#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import requests
import subprocess
import socket

def check_port(port):
    """检查端口是否被占用"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0
    except:
        return False

def test_api_connection(port=8000):
    """测试API连接"""
    try:
        response = requests.get(f"http://localhost:{port}/", timeout=5)
        return response.status_code == 200, response.text
    except requests.exceptions.ConnectionError:
        return False, "连接被拒绝"
    except requests.exceptions.Timeout:
        return False, "连接超时"
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 50)
    print("植物识别API服务诊断工具")
    print("=" * 50)
    
    # 检查Python环境
    print(f"Python版本: {sys.version}")
    print(f"当前工作目录: {os.getcwd()}")
    
    # 检查虚拟环境
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ 虚拟环境已激活")
    else:
        print("❌ 虚拟环境未激活")
    
    # 检查依赖
    print("\n检查依赖包...")
    try:
        import fastapi
        print(f"✅ FastAPI版本: {fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI未安装")
        return
    
    try:
        import uvicorn
        print(f"✅ Uvicorn版本: {uvicorn.__version__}")
    except ImportError:
        print("❌ Uvicorn未安装")
        return
    
    try:
        import plantid
        print("✅ 植物识别模块已安装")
    except ImportError:
        print("❌ 植物识别模块未安装")
        return
    
    # 检查端口
    print(f"\n检查端口8000...")
    if check_port(8000):
        print("❌ 端口8000已被占用")
        
        # 尝试找到占用端口的进程
        try:
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if ':8000' in line:
                    print(f"占用进程信息: {line}")
        except:
            print("无法获取进程信息")
    else:
        print("✅ 端口8000可用")
    
    # 测试API连接
    print(f"\n测试API连接...")
    success, message = test_api_connection()
    if success:
        print(f"✅ API服务正常运行: {message}")
    else:
        print(f"❌ API服务无法访问: {message}")
    
    # 建议解决方案
    print("\n" + "=" * 50)
    print("建议解决方案:")
    print("1. 确保虚拟环境已激活")
    print("2. 运行: python test_api.py")
    print("3. 检查防火墙设置")
    print("4. 尝试使用不同端口")
    print("=" * 50)

if __name__ == "__main__":
    main() 