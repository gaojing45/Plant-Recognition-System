#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

# 导入植物识别模块
import plantid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# 全局植物识别器
plant_identifier = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_plant_identifier():
    """初始化植物识别器"""
    global plant_identifier
    if plant_identifier is None:
        try:
            plant_identifier = plantid.PlantIdentifier()
            print("植物识别器初始化成功")
        except Exception as e:
            print(f"植物识别器初始化失败: {e}")
            return False
    return True

def image_to_base64(image):
    """将OpenCV图像转换为base64字符串"""
    if image is None:
        return None
    
    # 转换BGR到RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 转换为PIL图像
    pil_image = Image.fromarray(image_rgb)
    
    # 转换为base64
    buffer = BytesIO()
    pil_image.save(buffer, format='JPEG', quality=85)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/jpeg;base64,{img_str}"

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """处理图片上传和识别"""
    if 'file' not in request.files:
        return jsonify({'error': '没有选择文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': '不支持的文件格式'}), 400
    
    try:
        # 初始化识别器
        if not init_plant_identifier():
            return jsonify({'error': '植物识别器初始化失败'}), 500
        
        # 读取图片
        file_content = file.read()
        nparr = np.frombuffer(file_content, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': '无法读取图片'}), 400
        
        # 记录开始时间
        start_time = time.time()
        
        # 进行植物识别
        outputs = plant_identifier.identify(image, topk=5)
        
        # 计算处理时间
        process_time = time.time() - start_time
        
        if outputs['status'] != 0:
            return jsonify({'error': outputs['message']}), 500
        
        # 准备结果
        results = []
        for i, result in enumerate(outputs['results']):
            results.append({
                'rank': i + 1,
                'chinese_name': result['chinese_name'],
                'latin_name': result['latin_name'],
                'probability': round(result['probability'] * 100, 2),
                'confidence': '高' if result['probability'] > 0.8 else '中' if result['probability'] > 0.5 else '低'
            })
        
        # 转换图片为base64用于显示
        image_base64 = image_to_base64(image)
        
        # 保存识别记录
        record = {
            'timestamp': datetime.now().isoformat(),
            'filename': secure_filename(file.filename),
            'process_time': round(process_time, 3),
            'results': results
        }
        
        return jsonify({
            'success': True,
            'image': image_base64,
            'results': results,
            'process_time': round(process_time, 3),
            'record': record
        })
        
    except Exception as e:
        return jsonify({'error': f'处理失败: {str(e)}'}), 500

@app.route('/batch', methods=['POST'])
def batch_upload():
    """批量上传处理"""
    if 'files[]' not in request.files:
        return jsonify({'error': '没有选择文件'}), 400
    
    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    # 初始化识别器
    if not init_plant_identifier():
        return jsonify({'error': '植物识别器初始化失败'}), 500
    
    results = []
    total_time = 0
    
    for file in files:
        if file and allowed_file(file.filename):
            try:
                # 读取图片
                file_content = file.read()
                nparr = np.frombuffer(file_content, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if image is not None:
                    start_time = time.time()
                    outputs = plant_identifier.identify(image, topk=3)
                    process_time = time.time() - start_time
                    total_time += process_time
                    
                    if outputs['status'] == 0:
                        top_result = outputs['results'][0]
                        results.append({
                            'filename': secure_filename(file.filename),
                            'chinese_name': top_result['chinese_name'],
                            'latin_name': top_result['latin_name'],
                            'probability': round(top_result['probability'] * 100, 2),
                            'process_time': round(process_time, 3)
                        })
                    else:
                        results.append({
                            'filename': secure_filename(file.filename),
                            'error': outputs['message']
                        })
                        
            except Exception as e:
                results.append({
                    'filename': secure_filename(file.filename),
                    'error': str(e)
                })
    
    return jsonify({
        'success': True,
        'results': results,
        'total_time': round(total_time, 3),
        'total_files': len(results)
    })

@app.route('/api/identify', methods=['POST'])
def api_identify():
    """API接口 - 图片识别"""
    if 'image' not in request.files:
        return jsonify({'error': '没有图片文件'}), 400
    
    file = request.files['image']
    topk = request.form.get('topk', 5, type=int)
    
    try:
        # 初始化识别器
        if not init_plant_identifier():
            return jsonify({'error': '植物识别器初始化失败'}), 500
        
        # 读取图片
        file_content = file.read()
        nparr = np.frombuffer(file_content, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': '无法读取图片'}), 400
        
        # 进行识别
        outputs = plant_identifier.identify(image, topk=topk)
        
        if outputs['status'] != 0:
            return jsonify({'error': outputs['message']}), 500
        
        # 格式化结果
        results = []
        for result in outputs['results']:
            results.append({
                'chinese_name': result['chinese_name'],
                'latin_name': result['latin_name'],
                'probability': result['probability']
            })
        
        return jsonify({
            'status': 'success',
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """健康检查接口"""
    try:
        if init_plant_identifier():
            return jsonify({'status': 'healthy', 'message': '服务正常运行'})
        else:
            return jsonify({'status': 'unhealthy', 'message': '植物识别器未初始化'}), 500
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'message': str(e)}), 500

if __name__ == '__main__':
    print("正在启动植物识别Web服务...")
    print("访问地址: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 