#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import collect_fea_style as cfs
import img_style_transform as ist
import time
import painting_split as ps

app = Flask(__name__)
 
UPLOAD_FOLDER_content = 'static/uploads/content'
UPLOAD_FOLDER_style = 'static/uploads/style'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER_content'] = UPLOAD_FOLDER_content
app.config['UPLOAD_FOLDER_style'] = UPLOAD_FOLDER_style
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(file):
    file_content = file
    file_cname = file_content.filename
    a = '.' in file_cname and file_cname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return a
     
 
@app.route('/')
def home():
    return render_template('index.html')
 

@app.route('/', methods=['POST'])
def upload_image():
    if_style = 'no'
    if_painting = 'no'
    content_path =''
    style_path=''
    output_path=''
    painting_content_path=''
    painting_output_path=''
    number_split = 'none'
    style_degree = '1'
    #style part
    sign_style = False
    sign_painting = False
    style_path = request.form.get('style_file') 
    if 'content_file' in request.files and style_path != '':
        sign_style = True
        content_file = request.files['content_file']
    #number_split = request.form.get('number_split')
    #print(number_split)
    if sign_style and allowed_file(content_file):
        style_degree= request.form.get('style_degree')
        style_degree = float(style_degree)
        print(style_degree)
        filename_content = secure_filename(content_file.filename)
        content_pure_name = filename_content.split('.')[0]
        style_pure_name  = style_path.split('/')[-1]
        style_pure_name = style_pure_name.split('.')[0]
        output_path = 'static/uploads/output/' + content_pure_name+'_'+style_pure_name +'.jpg'
        try:
            open(output_path,'rb')
        except:
            content_file.save(os.path.join(app.config['UPLOAD_FOLDER_content'], filename_content))
            cfs.style_model_train(style_pure_name)
            content_path ='static/uploads/content/'+filename_content
            ist.img_style_transform(content_path,content_pure_name,style_pure_name,style_degree)
            #print('upload_image filename: ' + filename)
            flash('Image successfully uploaded and displayed below')
        content_path = app.config['UPLOAD_FOLDER_content']+ '/'+ filename_content
        style_path = app.config['UPLOAD_FOLDER_style'] +'/' + style_pure_name +'.jpg'
        if_style = 'yes'

    #painting part
    if 'painting_content_file' in request.files:
        print('hold1')
        sign_painting= True
        painting_content_file = request.files['painting_content_file']
    #number_split = request.form.get('number_split')
    #print(number_split)
    if sign_painting and allowed_file(painting_content_file):
        print('hold2')
        filename_content = secure_filename(painting_content_file.filename)
        content_pure_name = filename_content.split('.')[0]
        number_split = request.form.get('number_split')
        painting_output_path = 'static/uploads/painting/' + content_pure_name+'_'+number_split+'splits.jpg'
        painting_content_path = app.config['UPLOAD_FOLDER_content']+ '/'+ filename_content
        try:
            open(painting_output_path,'rb')
        except:
            painting_content_file.save(os.path.join(app.config['UPLOAD_FOLDER_content'], filename_content))
            #print('upload_image filename: ' + filename)
            flash('Image successfully uploaded and displayed below')
            ps.split(painting_content_path,number_split,content_pure_name)
            
        if_painting = 'yes'


    params = {
        'style_photo': content_path,
        'style':style_path,
        'style_output' : output_path,
        'painting_photo':painting_content_path,
        'painting_output':painting_output_path,
        'if_style':if_style,
        'if_painting':if_painting,
        'number_split':number_split,
        'degree':style_degree
    }
    return render_template('index.html', **params)
 
if __name__ == "__main__":
    app.run()