#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import plantid
    print("✅ 植物识别模块导入成功！")
    
    # 测试创建识别器
    plant_identifier = plantid.PlantIdentifier()
    print("✅ 植物识别器创建成功！")
    
    print("\n🎉 部署成功！项目可以正常使用了。")
    print("\n使用方法：")
    print("1. 将图片放在 images/ 文件夹中")
    print("2. 运行: python demo.py")
    print("3. 或者使用Python接口:")
    print("   import cv2")
    print("   import plantid")
    print("   plant_identifier = plantid.PlantIdentifier()")
    print("   image = cv2.imread('your_image.jpg')")
    print("   outputs = plant_identifier.identify(image, topk=5)")
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
except Exception as e:
    print(f"❌ 其他错误: {e}") 