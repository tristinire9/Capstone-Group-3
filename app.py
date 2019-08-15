from flask import Flask, request, render_template
import boto3, botocore
import os

S3_BUCKET                 = os.environ.get("S3_BUCKET_NAME")
S3_KEY                    = os.environ.get("S3_ACCESS_KEY")
S3_SECRET                 = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
s3 = boto3.client(
        "s3",
        aws_access_key_id=S3_KEY,
        aws_secret_access_key=S3_SECRET)

app = Flask(__name__)


@app.route('/upload',methods = ["POST"])
def uploadFunc():
    if 'file' in request.files:
        file = request.files['file']
        print(open(file))
        try:
            s3.upload_fileobj(file,S3_BUCKET,file.filename,ExtraArgs={"ContentType": file.content_type})
        except:
            return "faileed"
        return str(file)


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
