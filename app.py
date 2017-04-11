from flask import Flask
from flask import render_template

ROOT_PATH = ''

app = Flask(__name__, static_url_path=ROOT_PATH + '/static')

UPLOAD_FOLDER = './'


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', ROOT_PATH=ROOT_PATH)


if __name__ == "__main__":
    app.run(port=80, debug=0)
