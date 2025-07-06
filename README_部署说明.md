# 植物识别项目部署说明（不使用conda）

## 方案一：使用批处理文件自动部署（推荐）

1. **确保Python已安装在 E:\python\**
   - 当前检测到Python版本：3.13.2 ✅
   - 如果路径不同，请修改脚本中的 `PYTHON_PATH`

2. **运行自动部署脚本**
   ```bash
   # 双击运行（推荐）
   deploy_without_conda.bat
   
   # 或者使用详细部署脚本
   手动部署.bat
   ```

3. **运行演示**
   ```bash
   # 双击运行
   run_demo.bat
   ```

## 方案二：手动部署

### 1. 安装Python
- 下载并安装Python 3.6或更高版本
- 确保安装时勾选"Add Python to PATH"

### 2. 创建虚拟环境
```bash
python -m venv plantid_env
```

### 3. 激活虚拟环境
```bash
# Windows
plantid_env\Scripts\activate.bat

# Linux/Mac
source plantid_env/bin/activate
```

### 4. 安装依赖
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. 运行演示
```bash
python demo.py
```

## 项目依赖说明

项目依赖的包：
- `opencv-python>=4.4` - 图像处理
- `pillow` - 图像处理
- `khandy>=0.1.8` - 工具库
- `onnxruntime==1.11.0` - ONNX模型推理

## 使用方法

### Python接口
```python
import cv2
import plantid

plant_identifier = plantid.PlantIdentifier()
image = cv2.imread('your_image.jpg')
outputs = plant_identifier.identify(image, topk=5)
if outputs['status'] == 0:
    print(outputs['results'])
```

### 演示程序
- 将图片放在 `images/` 文件夹中
- 运行 `python demo.py`
- 程序会显示识别结果和置信度

## 注意事项

1. **Python版本要求**：Python 3.6或更高版本
2. **内存要求**：模型大小约29.5MB
3. **识别能力**：支持4,066种植物分类
4. **准确率**：top1准确率84.8%，top5准确率95.9%

## 故障排除

### 问题1：找不到Python
- 确保Python已正确安装
- 检查环境变量PATH中是否包含Python路径

### 问题2：pip安装失败
- 尝试使用国内镜像：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/`

### 问题3：模型文件缺失
- 确保 `plantid/models/` 文件夹中包含所有模型文件
- 检查网络连接，模型文件可能需要下载

## 项目特点

- ✅ 开源模型，易于使用
- ✅ 支持4,066种植物分类
- ✅ 模型体积小（29.5MB）
- ✅ 高准确率（top1: 84.8%, top5: 95.9%）
- ✅ 持续更新维护 