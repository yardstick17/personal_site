import os

from flask import Flask, request
from flask import flash
from flask import redirect
from flask import render_template
from flask import send_from_directory
from flask import url_for
from werkzeug.utils import secure_filename

ROOT_PATH = ''

app = Flask(__name__, static_url_path=ROOT_PATH + '/static')

UPLOAD_FOLDER = './'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', ROOT_PATH=ROOT_PATH)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/temp', methods=['GET', 'POST'])
def temp():
    return render_template('temp.html', ROOT_PATH=ROOT_PATH)

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    return render_template('blog.html', ROOT_PATH=ROOT_PATH)


ROOT_PATH = '/'


@app.route('/upload/image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print('filename :::::', filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == "__main__":
    app.run(port=5002, debug=1)
