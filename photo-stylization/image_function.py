import tensorflow as tf

def load_img(img_path,maxdim = 800):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img,channels=3)
    img = tf.image.convert_image_dtype(img,tf.float32)
    shape = tf.cast(tf.shape(img)[:-1],tf.float32)
    long_dim = max(shape)
    scale = maxdim/long_dim
    new_shape = tf.cast(shape*scale,tf.int32)
    img = tf.image.resize(img,new_shape)
    img = img[tf.newaxis,:]
    return img