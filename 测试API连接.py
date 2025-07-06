#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

def test_api():
    """测试API服务"""
    base_url = "http://localhost:8000"
    
    print("=" * 50)
    print("测试植物识别API服务")
    print("=" * 50)
    
    # 测试根路径
    try:
        response = requests.get(f"{base_url}/")
        print(f"✓ 根路径测试: {response.status_code}")
        print(f"  响应: {response.json()}")
    except Exception as e:
        print(f"✗ 根路径测试失败: {e}")
    
    print()
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✓ 健康检查: {response.status_code}")
        data = response.json()
        print(f"  状态: {data['status']}")
        print(f"  消息: {data['message']}")
        print(f"  模型加载: {data['model_loaded']}")
    except Exception as e:
        print(f"✗ 健康检查失败: {e}")
    
    print()
    
    # 测试API文档
    try:
        response = requests.get(f"{base_url}/docs")
        print(f"✓ API文档: {response.status_code}")
        print(f"  文档地址: {base_url}/docs")
    except Exception as e:
        print(f"✗ API文档访问失败: {e}")
    
    print()
    print("=" * 50)
    print("API服务测试完成")
    print("=" * 50)

if __name__ == "__main__":
    test_api() 