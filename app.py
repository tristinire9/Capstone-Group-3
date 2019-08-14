from flask import Flask, request, url_for, redirect

app = Flask(__name__)


@app.route('/', methods = ["GET","POST"])
def hello_world():
    return request.method


if __name__ == '__main__':
    app.run()
