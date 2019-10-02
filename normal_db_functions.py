import sqlite3
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            isolation_level=None,
            detect_types=0
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def create_component(conn, component):
    """
    Create a new component into the components table
    :param conn: a database connection
    :param component: a component as a tuple
    :return: component id
    """
    sql = ''' INSERT INTO components ('name', 'version_num', 'date', 'url')
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, component)
    return cur.lastrowid


# connection = create_connection("../instance/flaskr.sqlite")
# id = create_component(connection, ('Thomas','1.4.3','2019-09-16','www.google.com'))
# print(id)


# check whether there is any duplicate, if there is, return True, otherwise False
def check_duplicate(fileName, versionNumber):
    """ check whether there is any duplicate with both fileName and versionNumber
        in db_file
    :param db_file: database file
    :param fileName: name of a component
    :param versionNumber: version number of a component
    :return: True or False
    """
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM components WHERE name = ? AND version_num = ?", (fileName, versionNumber))
    data = cursor.fetchall()
    if len(data) == 0:
        return False
    else:
        return True

def get_URL(fileName, versionNumber):
    cursor = get_db().cursor()
    cursor.execute("SELECT url FROM components WHERE name = ? AND version_num = ?", (fileName, versionNumber))
    data = cursor.fetchall()
    if len(data) == 0:
        return None
    else:
        return data

# return a list containing all components' names
def all_components_names():
    """ return a list containing all components' names in db_file
    :param db_file: database file
    :return: a list
    """
    cursor = get_db().cursor()
    cursor.execute("SELECT DISTINCT name FROM components")
    all_components = cursor.fetchall()

    component_names_list = []
    for component in all_components:
        component_names_list.append(component[0]) #adds into index at which it's ID(PK) is represented
    return component_names_list


# return a list containing all the version numbers of a specific component
def lookup( componentName):
    """ return a list containing all the version numbers of a specific component in db_file
    :param db_file: database file
    :param componentName: name of a component
    :return: a list
    """
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM components WHERE name = ? ", (componentName,))
    components = cursor.fetchall()

    versionNumbers = []
    for component in components:
        versionNumbers.append(component[2])

    return versionNumbers

def lookupRecipe(recipeID):
    """ return a list containing all the version numbers of a specific component in db_file
    :param db_file: database file
    :param componentName: name of a component
    :return: a list
    """
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM recipes WHERE id = ? ", (recipeID,))
    recipes = cursor.fetchall()
    return recipes[0] if recipes else None

def delete_component(name, version_num):
    cursor = get_db().cursor()
    cursor.execute("DELETE FROM components WHERE name = ? AND version_num = ?", (name, version_num))
    return 0

def create_recipe(name, version_num, status):
    cursor = get_db().cursor()
    cursor.execute(''' INSERT INTO recipes ('name', 'version_num', 'status')
              VALUES(?,?,?) ''', (name, version_num, status))
    return 0

def update_recipe(id, name, version_num, status):
    cursor = get_db().cursor()
    cursor.execute(''' UPDATE recipes
              SET name = ? ,
                  version_num = ? ,
                  status = ?
              WHERE id = ? ''', (name, version_num, status, id))
    return 0

def all_Recipes():
    """Returns a list of all recipe names"""
    cursor = get_db().cursor()
    cursor.execute("SELECT id, name FROM recipes")
    all_recipes = cursor.fetchall()
    return all_recipes

def create_relationship(componentID, recipeID):
    cursor = get_db().cursor()
    cursor.execute(''' INSERT INTO relationships ('componentID', 'recipeID')
                  VALUES(?,?) ''', (componentID, recipeID))
    return 0
# create_component(create_connection("../instance/myDB"), ("Thomas", "1.2.3.4", "19/9/2019", "www.google.com"))
# print(lookup("../instance/myDB", "Thomas"))
