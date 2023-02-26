import numpy as np
import cv2
import tflite_runtime.interpreter as tflite
import os

# 风格特征提取模型
file_model_prediction = "model/magenta_arbitrary-image-stylization-v1-256_int8_prediction_1.tflite"
base_path ="static/uploads/style"

def img_preprocessing(img,size_output):
    # 获取图像的尺寸
    imH,imW,_ = np.shape(img)

    # BGR 转RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 尺寸缩放适应网络输入要求
    img_resized = cv2.resize(img_rgb, size_output)

    # 维度扩张适应网络输入要求
    input_data = np.expand_dims(img_resized, axis=0)
    
    # 正则化变为 0-1之间
    input_data = input_data/255.0
    
    return (imW,imH), np.float32(input_data)
    
# 从风格图片中提取风格特征矢量.
def run_style_predict(file_model_prediction,img):

    # 加载模型
    interpreter = tflite.Interpreter(model_path=file_model_prediction)
    interpreter.allocate_tensors()
  
    # 获取输入的数据的信息
    input_details = interpreter.get_input_details()
    
    # 获取输入图像的高和宽
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    
    # 对图像进行预处理
    t,preprocessed_style_image = img_preprocessing(img,(width,height))
    
    # 特征输入网络
    interpreter.set_tensor(input_details[0]["index"], preprocessed_style_image)

    # 获取模型矢量.
    interpreter.invoke()

    style_bottleneck = interpreter.tensor(interpreter.get_output_details()[0]["index"])()

    return style_bottleneck


def style_model_train(style_name):
    # 遍历文件夹
    # if alreaday contain then return
    feature_path = 'static/uploads/style_model/' +style_name+'.npz'
    if os.path.isfile(feature_path):
        return
    for f_img in os.listdir(base_path):
        # 遍历所有以.jpg为后缀的文件
        if os.path.splitext(f_img)[-1] == ".jpg" and os.path.splitext(f_img)[0] == style_name:
            str_style =  os.path.splitext(f_img)[0]
            print(str_style)
            f_img = os.path.join(base_path,f_img)
            
            # 提取风格特征
            style_bottleneck = run_style_predict(file_model_prediction,cv2.imread(f_img))
            
            # 特征保存
            print('save style feature of image %s as %s.npz'%(f_img,os.path.join('static/uploads/style_model',str_style)))
            
            np.savez(os.path.join('static/uploads/style_model',str_style),fea = style_bottleneck)
            
            
        
 