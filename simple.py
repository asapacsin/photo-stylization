import tensorflow as tf
import matplotlib.pyplot as plt
import os
from PIL import Image
import numpy
import time
from datetime import timedelta


style_layers = ['block1_conv1','block2_conv1','block3_conv1','block4_conv1','block5_conv1']
content_layers = ['block5_conv2']

def load_img(img_path,max_dim=800):
    #use tensorflow to read image
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img,channels=3,dtype=tf.float32)
    #rearrange the image
    shape = tf.cast(tf.shape(img)[:-1],tf.float32)
    long_len = max(shape)
    scale = max_dim/long_len
    new_shape = tf.cast(scale*shape,tf.int32)
    img = tf.image.resize(img,new_shape)
    img = img[tf.newaxis,:]
    return img

def show_img(img,title=None):
    #remove excess dimension
    if len(img.shape)>3:
        img = tf.squeeze(img)
    plt.imshow(img)
    plt.axis('off')
    if title:
        plt.title(title)
    plt.show()

def vgg_layers(layer_names):
    vgg = tf.keras.applications.vgg16.VGG16(include_top=False,weights='imagenet')
    vgg.trainable = False
    output = [vgg.get_layer(name).output for name in layer_names]
    model = tf.keras.Model([vgg.input],output)
    return model

def gram_matrix(tensor):
    res = tf.linalg.einsum('bijc,bijd->bcd',tensor,tensor)
    shape = tf.shape(tensor)
    num_features = tf.cast(shape[1]*shape[2],tf.float32)
    return res/num_features

class StyleContentModel(tf.keras.models.Model):
    def __init__(self,style_layers,content_layers):
        super(StyleContentModel,self).__init__()
        self.vgg = vgg_layers(style_layers+content_layers)
        self.style_layers = style_layers
        self.content_layers = content_layers
        self.num_style_layers = len(style_layers)

    def call(self,input):
        preprocess_input = tf.keras.applications.vgg16.preprocess_input(input*255)
        output = self.vgg(preprocess_input)
        style_output,content_output = output[:self.num_style_layers],output[self.num_style_layers:]
        #would use the gram_matrix of style to do the loss evaluation
        style_output = [gram_matrix(i) for i in style_output]
        style_dict = {name:value for name,value in zip(self.style_layers,style_output)}
        content_dict ={name:value for name,value in zip(self.content_layers,content_output)}
        return {'style':style_dict,'content':content_dict}

extrator = StyleContentModel(style_layers,content_layers)

def StyleContentLoss(output,style_weight,content_weight,style_target,content_target,num_style_layers,num_content_layers):
    style_output = output['style']
    content_output = output['content']
    style_loss = sum([tf.reduce_mean((style_output[name]-style_target[name])**2) for name in style_output.keys()])
    style_loss *= style_weight/num_style_layers
    content_loss = sum([tf.reduce_mean((content_output[name]-content_target[name])**2) for name in content_output.keys()])
    content_loss *= content_weight/num_content_layers
    loss = style_loss + content_loss
    return loss

def clip_0_1(image):
    return tf.clip_by_value(image,clip_value_max=1.0,clip_value_min=0.0)

def TotalVariationLoss(image):
    x_delta = image[:,:,1:,:] - image[:,:,:-1,:]
    y_delta = image[:,1:,:,:] - image[:,:-1,:,:]
    return tf.reduce_mean(x_delta**2) + tf.reduce_mean(y_delta**2)

def trainstep(image,variation_weight,style_weight,content_weight,style_target,content_target,num_style_layers,num_content_layers,opt):
    with tf.GradientTape() as tape:
        output = extrator(image)
        loss = StyleContentLoss(output,style_weight,content_weight,style_target,content_target,num_style_layers,num_content_layers)
        loss += variation_weight*TotalVariationLoss(image)
    grad = tape.gradient(loss,image)
    opt.apply_gradients([(grad,image)])
    image.assign(clip_0_1(image))

def save_img(image,img_name):
    if len(image.shape)>3:
        image = tf.squeeze(image)
    image = image*255
    image = image.numpy().astype('uint8')
    image = Image.fromarray(image)
    os.makedirs('save_img',exist_ok=True)
    image.save('save_img/'+img_name+'.jpg')

def style(content_path,style_path,output_path):
    variation_weight = 1e5
    style_weight = 10
    content_weight = 1
    epochs = 101
    max_dim = 256
    style_image = load_img(style_path,max_dim)
    content_image = load_img(content_path,max_dim)
    opt = tf.optimizers.Adam(learning_rate=0.02,beta_1=0.99,epsilon=1e-1)
    
    num_style_layers = len(style_layers)
    num_content_layers = len(content_layers)
    
    content_target = extrator(content_image)['content']
    style_target = extrator(style_image)['style']
    #noise_img = load_img('noise/noise.jpg',max_dim=1440)
    image = tf.Variable(content_image)
    os.makedirs('output',exist_ok=True)
    current_time = time.time()
    local_time = time.localtime(current_time)
    dt = time.strftime('%Y:%m:%d %H:%M:%S',local_time)
    print('current time is ',str(dt))
    print('start simple')
    for n in range(epochs):
        trainstep(image,variation_weight,style_weight,content_weight,style_target,content_target,num_style_layers,num_content_layers,opt)
        if n%10 == 0:
            print(n)
    get_img = tf.squeeze(image)
    get_img = Image.fromarray(numpy.uint8(get_img.numpy()*255))
    get_img.save(output_path)
    end_time = time.time()
    use_time = end_time-current_time
    use_time = int(use_time)
    use_time = timedelta(seconds=use_time)
    print('use time:',str(use_time))
    local_time = time.localtime(end_time)
    dt = time.strftime('%Y:%m:%d %H:%M:%S',local_time)
    print('the local time is ',str(dt))