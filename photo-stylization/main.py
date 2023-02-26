#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import collect_fea_style as cfs
import img_style_transform as ist
import time

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
    start = time.process_time()
    print('get something')
    style_degree= request.form.get('style_degree')
    style_degree = float(style_degree)
    print(style_degree)
    style_path = request.form.get('style_file')
    if 'content-file'not in request.files and style_path == "":
        flash('No file part')
        return redirect(request.url)
    content_file = request.files['content-file']
    if content_file and allowed_file(content_file):
        filename_content = secure_filename(content_file.filename)
        content_pure_name = filename_content.split('.')[0]
        style_pure_name  = style_path.split('/')[-1]
        style_pure_name = style_pure_name.split('.')[0]
        content_file.save(os.path.join(app.config['UPLOAD_FOLDER_content'], filename_content))
        cfs.style_model_train(style_pure_name)
        content_path ='static/uploads/content/'+filename_content
        ist.img_style_transform(content_path,content_pure_name,style_pure_name,style_degree)
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        content_path = app.config['UPLOAD_FOLDER_content']+ '/'+ filename_content
        style_path = app.config['UPLOAD_FOLDER_style'] +'/' + style_pure_name +'.jpg'
        output_path = 'static/uploads/output/' + content_pure_name+'_'+style_pure_name +'.jpg'
        params = {
            'content': content_path,
            'style':style_path,
            'output' : output_path
        }
        end = time.process_time()
        print('the time cost is '+str(end-start)+'seconds')
        return render_template('success.html', **params)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
if __name__ == "__main__":
    app.run()