#from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
#from flask_bootstrap import Bootstrap
#from filters import datetimeformat, file_type
#from resources import get_bucket, get_buckets_list

#app = Flask(__name__)
#app.add_template_filter(datetimeformat)
#pp.add_template_filter(file_type)
#bootstrap = Bootstrap(app)
from auth import bp

import db
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash, \
    Response, session
from flask_bootstrap import Bootstrap
from filters import datetimeformat, file_type
from resources import get_bucket, get_buckets_list

app = Flask(__name__)
db.init_app(app)
app.register_blueprint(bp, url_prefix="/hi")
app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
Bootstrap(app)
app.secret_key = 'secret'
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type

# @app.route('/hello')
# def hello():
#     return 'Hello, World!'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bucket = request.form['bucket']
        session['bucket'] = bucket
        return redirect(url_for('files'))
    else:
        buckets = get_buckets_list()
        return render_template("index.html", buckets=buckets)

@app.route('/files')
def files():
    my_bucket = get_bucket()
    summaries = my_bucket.objects.all()
    return render_template('files.html', my_bucket=my_bucket, files=summaries)


@app.route('/component', methods=['POST'])
def component():
    file = request.files['file']

    my_bucket = get_bucket()
    my_bucket.Object(file.filename).put(Body=file)



    #flash('File uploaded successfully')
    return redirect(url_for('files'))

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    my_bucket = get_bucket()
    my_bucket.Object(file.filename).put(Body=file)

    flash('File uploaded successfully')
    return redirect(url_for('files'))

@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    my_bucket = get_bucket()
    my_bucket.Object(key).delete()

    flash('File deleted successfully')
    return redirect(url_for('files'))


@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']
    if not key:
        key = request.data['key']
    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )

if __name__ == '__main__':
#    app.secret_key = '\xd3#d\xb0\xfck=\x14\xb9qi\xde\x04\xea\xb9\x89\x02+\xd8\x1e8g\x83t' #this is new, had errors about needing a secret key
#    app.config['SESSION_TYPE'] = 'filesystem' #this is new
    app.run()
