import datetime
from auth import bp
import db

import normal_db_functions
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, \
    Response, session
from flask_bootstrap import Bootstrap
from datetime import datetime

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


@app.route('/', methods=['GET', 'POST'])  # Index page, shows list of buckets
def index():
    if request.method == 'POST':
        bucket = request.form['bucket']
        session['bucket'] = bucket
        return redirect(url_for('files'))
    else:
        buckets = get_buckets_list()
        return render_template("index.html", buckets=buckets)


@app.route('/files')  # Displays all components
def files():
    addToRecipe=request.args.get('addToRecipe')
    my_bucket = get_bucket()
    summaries = my_bucket.objects.all()
    components = normal_db_functions.all_components_names()
    return render_template('files.html', my_bucket=my_bucket, files=summaries, components = components,atR = addToRecipe)



@app.route('/component', methods=['POST'])  # Upload from Command line client
def component():
    file = request.files['file']
    filetype = file.filename.split(".")[1]
    ver = request.args.get('ver')
    fileName = request.args.get('Fname')
    URL = "https://capprojteam3.s3-ap-southeast-2.amazonaws.com/" + fileName + "".join(ver.split('.')) + '.' + filetype
    now = datetime.now()  # current date and time
    date_time = now.strftime("%d/%m/%Y, %H:%M:%S")

    connection = normal_db_functions.create_connection("instance/flaskr.sqlite")
    if normal_db_functions.check_duplicate("instance/flaskr.sqlite", fileName, ver):
        return jsonify("DUPLICATE"), 400
    normal_db_functions.create_component(connection, (fileName, ver, date_time, URL))

    my_bucket = get_bucket()
    my_bucket.Object(fileName + "".join(ver.split('.')) + '.' + filetype).put(Body=file)

    # flash('File uploaded successfully')
    return redirect(url_for('files'))


@app.route('/upload', methods=['POST'])  # Upload from Web UI
def upload():
    file = request.files['file']

    my_bucket = get_bucket()
    my_bucket.Object(file.filename).put(Body=file)

    flash('File uploaded successfully')
    return redirect(url_for('files'))


@app.route('/submitNewRecipe', methods=['GET'])  # API for adding new recipe to database
def submitNewRecipe():
    name = request.args.get('softwareName')
    ver = request.args.get('version')
    status = request.args.get('status')
    normal_db_functions.create_recipe(name, ver, status)
    flash('Recipe uploaded successfully')
    return redirect(url_for('files'))


@app.route('/updateRecipe', methods=['POST'])  # API for adding new recipe to database
def updateRecipe():
    id = request.form.get('id')
    name = request.form.get('name')
    ver = request.form.get('version')
    status = request.form.get('status')
    normal_db_functions.update_recipe(id, name, ver, status)
    flash('Recipe update successfully')
    return redirect(url_for('recipes'))


@app.route('/delete', methods=['POST']) #Delete from bucket
def delete():
    key = request.form['key']

    my_bucket = get_bucket()
    my_bucket.Object(key).delete()

    flash('File deleted successfully')
    return redirect(url_for('files'))


@app.route('/download', methods=['POST'])  # download from Web UI
def download():
    key = request.form['key'].split('/')[-1][:-4]
    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )


@app.route('/version', methods=['POST'])  # See all versions of a particular component
def version():
    component = request.form['component']
    addToRecipe = request.form['atR']
    my_bucket = get_bucket()
    versions=normal_db_functions.lookup(component)
    return render_template('versions.html', my_bucket=my_bucket, componentName=component, versions=versions,atR=addToRecipe)


@app.route('/editRecipe', methods=['POST'])  # See all versions of a particular component
def editRecipe():
    recipeID = request.form['recipeID']
    recipe = normal_db_functions.lookupRecipe(recipeID)
    return render_template('editRecipe.html', recipe=recipe)


@app.route('/recipes')  # Look-up page for all recipes in Database
def recipes():
    recipes = normal_db_functions.all_Recipes()
    return render_template('recipes.html', recipes=recipes, dB = normal_db_functions)


@app.route('/new_Recipe')  # Links from recipes look-up to create a new recipe.
def new_Recipe():
    if request.args.get('softwareName') is not None:
        return redirect(url_for('submitNewRecipe', softwareName=request.args.get['softwareName'],
                                version=request.args.get['version'], status=request.args.get['status']))
    return render_template('newRecipe.html')

@app.route('/recipeDetails',methods=['POST']) #Expands a recipe to view components and details
def recipeDetails():
    return render_template('recipeDetails.html',dB = normal_db_functions, recipeName = request.form['recipeName'], recipePK = request.form['recipePK'], recipeVER = request.form['ver'] )

@app.route('/addComponentRecipe',methods=['POST']) #Adds a component to the currently selected Recipe
def addComponentRecipe():

    recipePK = request.form['recipe']
    componentName = request.form["componentName"]
    version = request.form["version"]
    print(recipePK,componentName,version)
    normal_db_functions.create_a_relationship("instance/flaskr.sqlite",recipePK,componentName,version)
    flash('Component added to Recipe successfully! Select another Component to keep adding more.')
    return redirect(url_for('files',addToRecipe = recipePK))


@app.route('/retrieve', methods=['GET'])  # Command Line retrieve API
def retrieve():
    ver = request.args.get('ver')
    fileName = request.args.get('Fname')

    connection = normal_db_functions.create_connection()
    if normal_db_functions.check_duplicate(fileName, ver):
        url = normal_db_functions.get_URL(fileName, ver)
        key = url[0][0].split("/")[-1]

        my_bucket = get_bucket()
        file_obj = my_bucket.Object(key).get()

        return Response(
            file_obj['Body'].read(),
            mimetype='text/plain',
            headers={"Content-Disposition": "attachment;filename={}".format(key)}
        )
    else:
        return jsonify("DOESN'T EXIST"), 404


if __name__ == '__main__':
    #    app.secret_key = '\xd3#d\xb0\xfck=\x14\xb9qi\xde\x04\xea\xb9\x89\x02+\xd8\x1e8g\x83t' #this is new, had errors about needing a secret key
    #    app.config['SESSION_TYPE'] = 'filesystem' #this is new
    app.run()
