
from flask import Flask, request, url_for, redirect,jsonify, render_template
from flask_request_params import bind_request_params

app = Flask(__name__)


@app.route('/file', methods = ["GET","POST"])
def file():
    method = request.method
    parameters = request.params
    files = request.files
    return str(parameters)


@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/1')
def f1():
    return render_template('page1.html')


@app.route('/2')
def f2():
    return render_template('page2.html')


@app.route('/3')
def f3():
    return render_template('page3.html')


@app.route('/4')
def f4():
    return render_template('page4.html')


if __name__ == '__main__':
    app.run()
