#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import time
import painting_split as ps

app = Flask(__name__)
 
UPLOAD_FOLDER_content = 'static/uploads/content'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER_content'] = UPLOAD_FOLDER_content
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(file):
    file_content = file
    file_cname = file_content.filename
    a = '.' in file_cname and file_cname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return a
     
 
@app.route('/')
def home():
    return render_template('painting.html')
 

@app.route('/', methods=['POST'])
def upload_image():
    start = time.process_time()
    print('get something')
    if 'content-file'not in request.files:
        flash('No file part')
        return redirect(request.url)
    content_file = request.files['content-file']
    if content_file and allowed_file(content_file) :
        filename_content = secure_filename(content_file.filename)
        content_pure_name = filename_content.split('.')[0]
        content_file.save(os.path.join(app.config['UPLOAD_FOLDER_content'], filename_content))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        content_path = app.config['UPLOAD_FOLDER_content']+ '/'+ filename_content
        number_split = request.form.get('number_split')
        ps.split(content_path,number_split,content_pure_name)
        output_path = 'static/uploads/painting/' + content_pure_name+'_'+number_split+'splits.jpg'
        params = {
            'content': content_path,
            'output' : output_path,
            'number_split':number_split
        }
        end = time.process_time()
        print('the time cost is '+str(end-start)+'seconds')
        return render_template('painting_result.html', **params)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
if __name__ == "__main__":
    app.run()