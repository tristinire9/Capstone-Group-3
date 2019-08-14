from flask import Flask, request
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route('/', methods = ["GET","POST"])
def hello_world():
    return "hello world"

@app.route('/upload',methods = ["POST"])
def uploadFunc():
    if 'file' in request.files:
        file = request.files['file']
        return str(file)


if __name__ == '__main__':
    app.run()
