import tensorflow as tf
from PIL import Image
import numpy
import time
from datetime import timedelta
from numpy import asarray

width=200
height=200
epochs = 101
variation_weight = 1e-1
style_weight = 1
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

def styleContentLoss(output_dict,target_style,target_content):
    new_style_output,new_content_output = output_dict['style'],output_dict['content']
    style_loss = tf.add_n([tf.reduce_mean((new_style-style)**2)/2 for new_style,style in zip(new_style_output,target_style)])*style_weight
    content_loss = tf.add_n([tf.reduce_mean((new_content-content)**2)/2 for new_content,content in zip(new_content_output,target_content)])*content_weight
    loss = style_loss + content_loss
    return loss

def variation_loss(output_image,):
    x_delta = output_image[:,:,1:,:] - output_image[:,:,:-1,:]
    y_delta = output_image[:,1:,:,:] - output_image[:,:-1,:,:]
    loss = (tf.reduce_mean(x_delta**2) + tf.reduce_mean(y_delta**2))*variation_weight
    return loss

def train(output_image,target_style,target_content,opt):
     with tf.GradientTape() as tape:
            output_dict = extrator(output_image)
            loss = styleContentLoss(output_dict,target_style,target_content)
            loss += variation_loss(output_image)
     grad = tape.gradient(loss,output_image)
     opt.apply_gradients([(grad,output_image)])
     output_image.assign(tf.clip_by_value(output_image,clip_value_min=0.0,clip_value_max=1.0))

def process_img(img_path):
    img = Image.open(img_path)
    img = img.convert('RGB')
    img = asarray(img)
    img = tf.convert_to_tensor(img)
    new_shape = tf.cast([width,height],tf.int32)
    img = tf.image.resize(img,new_shape)
    img = img[tf.newaxis,:]/255
    return img

class styleContentModel(tf.keras.models.Model):
    def __init__(self):
        super(styleContentModel,self).__init__()
        self.vgg = vgg16(style_layers+content_layers)
    def call(self,image):
        preprocess_input = tf.keras.applications.vgg16.preprocess_input(image*255)
        output = self.vgg(preprocess_input)
        style_output,content_output = output[:len(style_layers)],output[len(style_layers):]
        style_output = [new_gram_matrix(style) for style in style_output]
        output_dict = {'style':style_output,'content':content_output}
        return output_dict

extrator = styleContentModel()

def style(content_path,style_path,output_path):
    style_image = process_img(style_path)
    content_image = process_img(content_path)
    
    
    #initialize the target 
    content_dict = extrator(content_image)
    style_dict = extrator(style_image)
    target_content = content_dict['content']
    target_style = style_dict['style']



    output_image = tf.Variable(content_image)

    #do the gradient descent
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
