import image_function as i_f
import tensorflow as tf
import os
import numpy
from PIL import Image
from datetime import timedelta
import time
import copy

def ini_set(number_split = 5):
    if number_split<2:
        number_split = 2
    elif number_split>255:
        number_split = 255
    val = 0
    step = 255//number_split
    store_set = []
    while val<=255:
        store_set.append(val)
        val += step
    return store_set

def find_store_binary(val,store_set,l,r):
    if l==r:
        return l
    if l+1==r:
        if abs(val-store_set[l])<abs(val-store_set[r]):
            return l
        else:
            return r
    mid = (l+r)//2
    if val>store_set[mid]:
        return find_store_binary(val,store_set,mid,r)
    else:
        return find_store_binary(val,store_set,l,mid)

def find_store(val,store_set):
    l = 0
    r = len(store_set)-1
    return find_store_binary(val,store_set,l,r)



def find_val(val,store_set):
    i= find_store(val,store_set)
    return store_set[i]
            
def split(img_path,number_split,content_name):
    number_split = int(number_split)
    max_dim = 1440
    img_name = img_path.split('/')[-1].split('.')[0]
    img = i_f.load_img(img_path,max_dim)
    img = tf.squeeze(img)
    img = img.numpy()
    os.makedirs('painting',exist_ok=True)
    current_time = time.time()
    local_time = time.localtime(current_time)
    df = time.strftime('%Y:%m:%d %H:%M:%S',local_time)
    print('the current time is: '+str(df))
    n = 255 - number_split + 1
    print(n)
    store_set = ini_set(number_split)
    copy_img = copy.deepcopy(img)
    for i in range(copy_img.shape[0]):
        for j in range(copy_img.shape[1]):
            for k in range(copy_img.shape[2]):
                value = copy_img[i,j,k] *255
                copy_img[i,j,k] = find_val(value,store_set)
    
    get_img = Image.fromarray(numpy.uint8(copy_img))
    get_img.save('static/uploads/painting/'+content_name+'_'+str(number_split)+'splits.jpg')
    
    end_time = time.time()
    print('the time cost is: '+str(timedelta(seconds=end_time-current_time)))
    end_local_time = time.localtime(end_time)
    df = time.strftime('%Y:%m:%d %H:%M:%S',end_local_time)
    print('the end time is: '+str(df))

if __name__ == '__main__':
    split('content/purple hair -starry night.png',5)
