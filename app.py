import os

from flask import Flask, send_from_directory, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import datetime

app = Flask(__name__)
app.secret_key = b'12rvyhaksvfasfvo1vwlfavoyv2lyavfsalyv'

# Set the folder for uploaded files
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        files = request.files.getlist('files')
        if not files:
            flash('No selected files')
            return redirect(request.url)

        prefix = int(datetime.datetime.now().timestamp() * 10000)

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{prefix}_{filename}'))
        
        flash('Files successfully uploaded')
        return redirect(url_for('upload_file'))

    return render_template('index.html')
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)