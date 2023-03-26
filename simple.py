import tensorflow as tf
import os
from PIL import Image
import numpy
import time
from datetime import timedelta
from numpy import asarray

width=200
height=200
epochs = 101
variation_weight = 1e5
style_weight = 10
content_weight = 1
style_layers = ['block1_conv1','block2_conv1','block3_conv1','block4_conv1','block5_conv1']
content_layers = ['block5_conv2']


def vgg16(layer_names):
    vgg = tf.keras.applications.vgg16.VGG16(include_top=False,weights='imagenet')
    vgg.trainable = False
    layer_names = style_layers+content_layers
    outputs = [vgg.get_layer(name).output for name in layer_names]
    model = tf.keras.Model([vgg.input],outputs)
    return model

def new_gram_matrix(input):
    gram = tf.linalg.einsum('aijb,aijc->abc',input,input)
    shape = gram.shape
    num_features = tf.cast(shape[0]*shape[1],tf.float32)
    return gram/num_features

def styleContentLoss(image,target_style,target_content):
    vgg = vgg16(style_layers+content_layers)
    new_output = vgg(image)
    new_style_output,new_content_output = new_output[:len(style_layers)],new_output[len(style_layers):]
    new_style_output = [new_gram_matrix(style) for style in new_style_output]
    style_loss = tf.add_n([tf.reduce_mean((new_style-style)**2)/2 for new_style,style in zip(new_style_output,target_style)])*style_weight
    content_loss = tf.add_n([tf.reduce_mean((new_content-content)**2)/2 for new_content,content in zip(new_content_output,target_content)])*content_weight
    loss = style_loss + content_loss
    return loss

def train(output_image,target_style,target_content,opt):
     with tf.GradientTape() as tape:
            loss = styleContentLoss(output_image,target_style,target_content)
            x_delta = output_image[:,:,1:,:] - output_image[:,:,:-1,:]
            y_delta = output_image[:,1:,:,:] - output_image[:,:-1,:,:]
            loss += (tf.reduce_mean(x_delta**2) + tf.reduce_mean(y_delta**2))*variation_weight
     grad = tape.gradient(loss,output_image)
     opt.apply_gradients([(grad,output_image)])
     output_image.assign(tf.clip_by_value(output_image,clip_value_min=0.0,clip_value_max=1.0))

def style(content_path,style_path,output_path):
    vgg = vgg16(style_layers+content_layers)
   
    style_image = Image.open(style_path)
    content_image = Image.open(content_path)
    #convert content_image as rgb
    content_image = content_image.convert('RGB')
    #convert style_image as rgb
    style_image = style_image.convert('RGB')
    style_image = asarray(style_image)
    content_image = asarray(content_image)
    style_image = tf.convert_to_tensor(style_image)
    content_image = tf.convert_to_tensor(content_image)
    new_shape = tf.cast([width,height],tf.int32)
    style_image = tf.image.resize(style_image,new_shape)
    content_image = tf.image.resize(content_image,new_shape)
    style_image = style_image[tf.newaxis,:]/255

    content_image = content_image[tf.newaxis,:]/255
    
    
    #initialize the target 
    output = vgg(content_image)
    style_output = vgg(style_image)
    photo_style_output,photo_content_output = output[:len(style_layers)],output[len(style_layers):]
    style_output = style_output[:len(style_layers)]

    #process the style output by gram matrix
    photo_style_output = [new_gram_matrix(style) for style in photo_style_output]
    style_output = [new_gram_matrix(style) for style in style_output]

    #initialize the target image
    target_content = photo_content_output
    target_style = style_output

    output_image = tf.Variable(content_image)

    #do the gradient descent
    os.makedirs('output',exist_ok=True)
    opt = tf.optimizers.Adam(learning_rate=0.02,beta_1=0.99,epsilon=1e-1)
    current_time = time.time()
    local_time = time.localtime(current_time)
    dt = time.strftime('%Y:%m:%d %H:%M:%S',local_time)
    print('current time is ',str(dt))
    #loop epochs times
    
    for i in range(epochs):
        train(output_image,target_style,target_content,opt)
        if i%10 == 0:
            print(i)
            
    get_img = tf.squeeze(output_image)
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