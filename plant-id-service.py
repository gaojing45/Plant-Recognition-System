import os
import time
import cv2
import khandy
import numpy as np
import plantid
from fastapi import FastAPI
import urllib.request as request
import sys
sys.setrecursionlimit(3000)

def readurlimage(url:str=""):
    #url="http://127.0.0.1/profile/upload/2025/04/12/ala_20250412111239A003.jpg"
    #url="https://tse1-mm.cn.bing.net/th/id/OIP-C.WrLSSqDLTrCD5Svuax5GiQHaE8?rs=1&pid=ImgDetMain"
    res = request.urlopen(url)    
    print(res)
    img=np.asarray(bytearray(res.read()),dtype="uint8")
    print(img.shape)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    print(img.shape)
    #img=cv2.imdecode(img,cv2.IMREAD_COLOR)
    #print(img)
    return img
def  recognize_url(url):    
    image=readurlimage(url)
    #image = khandy.imread_cv(src_filename)
    plant_identifier = plantid.PlantIdentifier()
    outputs = plant_identifier.identify(image,topk=5)
    #start_time = time.time()
	#print('[{}] Time: {:.3f}s  {}'.format( len(src_filename), time.time() - start_time, name))
       
    if max(image.shape[:2]) > 1080:
        image = khandy.resize_image_long(image, 1080)
    if outputs['status'] == 0:
        print(outputs['results'][0])
        print(outputs['results'][1])
        print(outputs['results'][2])
    else:
        print(outputs)
    return outputs
def  recognize(src_filename):
    image = khandy.imread_cv(src_filename)
    print(type(image))
    plant_identifier = plantid.PlantIdentifier()
    outputs = plant_identifier.identify(image,topk=5)
    #start_time = time.time()
	#print('[{}] Time: {:.3f}s  {}'.format( len(src_filename), time.time() - start_time, name))
    
    
    if max(image.shape[:2]) > 1080:
        image = khandy.resize_image_long(image, 1080)
    if outputs['status'] == 0:
        print(outputs['results'][0])
        print(outputs['results'][1])
        print(outputs['results'][2])
    else:
        print(outputs)
    return outputs
app = FastAPI()
@app.get("/filepath/")
def recognizefile(path:str=""):
    result=recognize(path)
    return result
@app.get("/urlpath/")
def recognizeurl(path:str=""):
    result=recognize_url(path)
    return result
#url="https://tse1-mm.cn.bing.net/th/id/OIP-C.WrLSSqDLTrCD5Svuax5GiQHaE8?rs=1&pid=ImgDetMain"
#result=recognize_url(url)
#print(result)