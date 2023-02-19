import os
from flask import Flask, render_template,send_file, request, redirect, send_file
from werkzeug.utils import secure_filename

from config import DATA_PATH, UPLOAD_PATH


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/'+DATA_PATH)
def listing_file():
    files = os.listdir(DATA_PATH)
    return render_template('files.html', files=files)

@app.route('/'+DATA_PATH+'/<path:res_path>')
def get_file(res_path):
    abs_path = os.path.join(DATA_PATH, res_path)
    if os.path.isfile(abs_path):
        return send_file(abs_path)
    
    if os.path.isdir(abs_path):
        return render_template('files.html', files=os.listdir(abs_path))
    
    return redirect('/data')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')

    if request.method == 'POST':
        if 'files[]' not in request.files:
                return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_PATH, filename))
        
    return redirect('/upload')
    

if __name__ == '__main__':
    app.run(debug=True, port=5003)