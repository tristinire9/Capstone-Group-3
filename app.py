from flask import Flask, request, url_for, redirect,jsonify
from flask_request_params import bind_request_params

app = Flask(__name__)


@app.route('/', methods = ["GET","POST"])
def hello_world():
    method = request.method
    parameters = request.params
    return request.data


if __name__ == '__main__':
    app.run()
