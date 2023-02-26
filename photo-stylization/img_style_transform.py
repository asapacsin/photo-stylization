import numpy as np
import cv2
import tflite_runtime.interpreter as tflite
import os
from collect_fea_style import img_preprocessing,run_style_predict

# 风格特征提取模型
file_model_prediction = "model/magenta_arbitrary-image-stylization-v1-256_int8_prediction_1.tflite"
# 风格转换模型
file_model_transfer = "model/magenta_arbitrary-image-stylization-v1-256_int8_transfer_1.tflite"
# 进行风格转换 输入风格矢量 、 风格转换模型 、    

def run_style_transform(file_model_transfer,style_bottleneck, content_image):
    im_H,im_W,_ = np.shape(content_image)
    
    # 加载模型
    interpreter = tflite.Interpreter(model_path=file_model_transfer)
    interpreter.allocate_tensors()
    
    # 获取输入信息
    input_details = interpreter.get_input_details()
    
    # 获取输入图像的高和宽
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    
    # 对内容图像进行预处理
    t,preprocessed_content_image = img_preprocessing(content_image,(width,height))
    
    # 将数据送入模型.
    interpreter.set_tensor(input_details[0]["index"], preprocessed_content_image)
    interpreter.set_tensor(input_details[1]["index"], style_bottleneck)
    interpreter.invoke()

    # 得到风格变换后的图像.
    stylized_image = interpreter.tensor(interpreter.get_output_details()[0]["index"])()
    
    # 将输出从0-1 转为 0-255 浮点转uint8
    stylized_image = np.uint8(stylized_image*255)
    stylized_image = np.squeeze(stylized_image)
    # RGB 转 BGR
    stylized_image = cv2.cvtColor(stylized_image, cv2.COLOR_RGB2BGR)
    stylized_image = cv2.resize(stylized_image,(im_W,im_H))
    return stylized_image
def img_style_transform(content_path,content_image_name,style_image_name,style_degree):
    # 加载风格特征
    path_fea_style= 'static/uploads/style_model'
    path_img_style = "static/uploads/style"
    path_output = "static/uploads/output"
    output_name = content_image_name+'_'+style_image_name +'.jpg'
    str_style = style_image_name
    style_fea = np.load(os.path.join(path_fea_style,str_style+'.npz'))['fea']
    
    # 显示风格图片
    #img_style = cv2.imread(os.path.join(path_img_style,str_style+'.jpg'))
    #cv2.imshow("img_style",img_style)
    
    # 读取原始图像
    img = cv2.imread(content_path)
    # 获取图像帧的尺寸
    imH,imW,_ = np.shape(img)
    # 适当缩放
    img = cv2.resize(img,(int(imW*0.8),int(imH*0.8)))
    #cv2.imshow("img",img)
    
    # 获取内容图像的风格特征
    content_fea = run_style_predict(file_model_prediction,img)
    
    # 设置风格比例
    ratio =int(float(style_degree*100))
    mix_fea = ratio*0.01*style_fea +(1-ratio*0.01)*content_fea
    
    print("start processing Style=%s ratio=%d%%"%(str_style,ratio))
    stylized_image = run_style_transform(file_model_transfer,mix_fea, img)
    print("processing end")
    #cv2.putText(stylized_image,'Style: %s ratio:%d'%(str_style,ratio),
                                 #(5,30),cv2.FONT_HERSHEY_SIMPLEX, 
                                  #0.8,(255,255,0),1,cv2.LINE_AA)
    stylized_image_savepath = os.path.join(path_output,output_name)
    cv2.imwrite(stylized_image_savepath,stylized_image)
    #cv2.imshow('style', stylized_image)
    
    #flag = 0
    #while True:
        #if flag:
            # 进行风格转换
            #print("start processing Style=%s ratio=%d%%"%(str_style,ratio))
            #stylized_image = run_style_transform(file_model_transfer,mix_fea, img)
            #cv2.putText(stylized_image,'Style: %s ratio:%d'%(str_style,ratio),(5,30),
                        #cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,0),1,cv2.LINE_AA)
            #print("processing end")
            #flag =0        
        
        # 显示结果
        #cv2.imshow('style', stylized_image)
        # 获取按键
        #key=cv2.waitKey(10) & 0xFF 
        
        # 按s 切换风格
        #if key == ord('s'):
        #str_style = input('Enter your style name:')
        #file_style = os.path.join(path_fea_style,str_style+'.npz')
        #if not os.path.exists(file_style):
            #print('Can not find ' + file_style)  
        #else:
            #img_style = cv2.imread(os.path.join(path_img_style,str_style+'.jpg'))
            #cv2.imshow("img_style",img_style)
        
            #style_fea = np.load(file_style)['fea']
            #mix_fea = ratio*0.01*style_fea +(1-ratio*0.01)*content_fea
            #flag = 1
        #key =0
            
        #elif key == ord('r'):    
           #str_ratio = input('Enter your style ratio:')
           #ratio = float(str_ratio)
           #mix_fea = ratio*0.01*style_fea +(1-ratio*0.01)*content_fea
           #flag = 1
       #elif key == ord('q'):
            #break
