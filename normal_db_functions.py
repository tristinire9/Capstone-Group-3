import sqlite3
import os
from packaging import version


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


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file, isolation_level=None)
        conn.row_factory = sqlite3.Row
    except sqlite3.Error as e:
        print(e)
    return conn


# connection = create_connection("../instance/flaskr.sqlite")
# id = create_component(connection, ('Thomas','1.4.3','2019-09-16','www.google.com'))
# print(id)


# check whether there is any duplicate, if there is, return True, otherwise False
def check_duplicate(db_file, fileName, versionNumber):
    """ check whether there is any duplicate with both fileName and versionNumber
        in db_file
    :param db_file: database file
    :param fileName: name of a component
    :param versionNumber: version number of a component
    :return: True or False
    """
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM components WHERE name = ? AND version_num = ?", (fileName, versionNumber))
    data = cursor.fetchall()
    if len(data) == 0:
        return False
    else:
        return True


def get_URL(db_file, fileName, versionNumber):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM components WHERE name = ? AND version_num = ?", (fileName, versionNumber))
    data = cursor.fetchall()
    if len(data) == 0:
        return None
    else:
        return data


# return a list containing all components' names
def all_components_names(db_file):
    """ return a list containing all components' names in db_file
    :param db_file: database file
    :return: a list
    """
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM components")
    all_components = cursor.fetchall()

    component_names_list = []
    for component in all_components:
        component_names_list.append(component[0])  # adds into index at which it's ID(PK) is represented
    return component_names_list


# return a list containing all the version numbers of a specific component
def lookup(db_file, componentName):
    """ return a list containing all the version numbers of a specific component in db_file
    :param db_file: database file
    :param componentName: name of a component
    :return: a list
    """
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM components WHERE name = ? ", (componentName,))
    components = cursor.fetchall()

    versionNumbers = []
    for component in components:
        versionNumbers.append(component[2])

    return versionNumbers


def lookupRecipe(db_file, recipeID):
    """ return a list containing all the version numbers of a specific component in db_file
    :param db_file: database file
    :param componentName: name of a component
    :return: a list
    """
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes WHERE id = ? ", (recipeID,))
    recipes = cursor.fetchall()
    return recipes[0] if recipes else None


def lookupRecipesByName(db_file, recipeName):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM recipes WHERE name LIKE ?", ('%' + recipeName + '%',))
    recipe_Names = cursor.fetchall()
    recipes = []
    for i in recipe_Names:
        recipes.append([i[0], recipeVersions(db_file, i[0])])
    return recipes


def delete_component(db_file, name, version_num):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM components WHERE name = ? AND version_num = ?", (name, version_num))
    components = cursor.fetchall()
    pk = components[0][0]
    cursor.execute("DELETE FROM components WHERE id = ? ", (pk,))
    cursor.execute("DELETE FROM relationships WHERE componentID = ? ", (pk,))
    return 0


def create_recipe(db_file, name, version_num, status):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO recipes ('name', 'version_num', 'status')
              VALUES(?,?,?) ''', (name, version_num, status))
    return cursor.lastrowid


def update_recipe(db_file, id, name, version_num, status):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute(''' UPDATE recipes
              SET name = ? ,
                  version_num = ? ,
                  status = ?
              WHERE id = ? ''', (name, version_num, status, id))
    return 0


def all_Recipes(db_file):
    """Returns a list of all recipe names"""
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM recipes")
    recipe_Names = cursor.fetchall()
    all_recipes = []
    for i in recipe_Names:
        all_recipes.append([i[0], recipeVersions("instance/flaskr.sqlite", i[0])])
    return all_recipes


def create_relationship(db_file, recipeId, componentId):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO relationships ('recipeID', 'componentID')
              VALUES(?,?) ''', (recipeId, componentId))

    return cursor.lastrowid

#Updates a components' download destination within a software release (Recipe)
def update_Component_Download_Destination(db_file, recipe_id, component_id, location):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute(''' UPDATE relationships
              SET destination_path = ?
              WHERE componentID = ? AND recipeID = ?''', (location, component_id, recipe_id))
    return 0

def change_recipe_name(db_file, oldName, version_num, newName):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute(''' UPDATE recipes SET name = ? WHERE name = ? AND version_num = ?''',
                   (newName, oldName, version_num))

    return 0


def change_recipe_version_num(db_file, name, old_version_num, new_version_num):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute(''' UPDATE recipes SET version_num = ? WHERE name = ? AND version_num = ?''',
                   (new_version_num, name, old_version_num))

    return 0


def change_recipe_status(db_file, name, version_num, new_status):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute(''' UPDATE recipes SET status = ? WHERE name = ? AND version_num = ?''',
                   (new_status, name, version_num))

    return 0


def get_a_recipe_ID(db_file, name, version_num):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM recipes WHERE name=? AND version_num=?""", (name, version_num))
    recipe = cursor.fetchall()
    return recipe[0][0]

def select_recipe_components(db_file, recipeId):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM relationships WHERE recipeID = ?''', (recipeId,))
    relationships = cursor.fetchall()

    return relationships


def get_a_component_ID(db_file, name, version_num):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM components WHERE name=? AND version_num=?""", (name, version_num))
    component = cursor.fetchall()
    return component[0][0]


def create_a_relationship(db_file, recipe_ID, component_name, component_num):
    destination_path = ""
    component_ID = get_a_component_ID(db_file, component_name, component_num)

    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO relationships ('componentID', 'recipeID', 'destination_path')
              VALUES(?,?,?) ''', (component_ID, recipe_ID, destination_path))

    return 0


def create_relationship(db_file, recipeId, componentId):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO relationships ('recipeID', 'componentID')
              VALUES(?,?) ''', (recipeId, componentId))

    return cursor.lastrowid


def delete_a_relationship(db_file, recipe_ID, component_ID):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM relationships WHERE componentID = ? AND recipeID = ? ", (component_ID, recipe_ID))
    return 0


# return a list
def get_a_component_by_ID(db_file, component_ID):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM components WHERE id = ?", (component_ID,))
    component = cursor.fetchall()
    return list(component[0])


def select_recipe_components(db_file, recipeId):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM relationships WHERE recipeID = ?''', (recipeId,))
    relationships = cursor.fetchall()

    return relationships


def all_components_in_a_recipe(db_file, recipe_name, recipe_num):
    recipe_ID = get_a_recipe_ID(db_file, recipe_name, recipe_num)

    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM relationships WHERE recipeID = ?''', (recipe_ID,))
    relationships = cursor.fetchall()

    component_IDs_list = []
    destinations_list = []
    for relationship in relationships:
        component_IDs_list.append(relationship[1])
        destinations_list.append(relationship[3])

    components_list = []
    for component_ID in component_IDs_list:
        components_list.append(get_a_component_by_ID(db_file, component_ID))

    result_list = []
    for i in range(0, len(destinations_list)):
        component = components_list[i]
        destination = destinations_list[i]
        newer = are_there_newer_versions_of_this_component(db_file, component[1], component[2])
        component.append(destination)
        component.append(newer)
        result_list.append(component)

    return result_list


def recipeVersions(db_file, recipe_name):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT version_num FROM recipes WHERE name = ? ", (recipe_name,))
    components = cursor.fetchall()

    versionNumbers = []
    for component in components:
        versionNumbers.append([component[0], get_a_recipe_ID(db_file, recipe_name, component[0])])

    return versionNumbers


# True is empty, and False is not empty
def is_folder_empty(folder_address):
    if len(os.listdir(folder_address)) == 0:
        return True
    else:
        return False


# True means that there are new versions or a new version of this component, False otherwise
def are_there_newer_versions_of_this_component(db_file, component_name, component_version_num):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT version_num FROM components WHERE name = ? ", (component_name,))
    components = cursor.fetchall()

    all_version_numbers = []
    for component in components:
        all_version_numbers.append(component[0])

    for i in range(0, len(all_version_numbers)):
        all_version_numbers[i] = version.parse(all_version_numbers[i])

    present_version_number = version.parse(component_version_num)
    compare_results = []

    for version_number in all_version_numbers:
        if version_number > present_version_number:
            compare_results.append(True)
        else:
            compare_results.append(False)

    if True in compare_results:
        return True
    else:
        return False


# False means that there is no duplicate
def check_duplicate_recipes(db_file, recipe_name, recipe_version_number):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes WHERE name = ? AND version_num = ?", (recipe_name, recipe_version_number))
    data = cursor.fetchall()
    if len(data) == 0:
        return False
    else:
        return True
# create_component(create_connection("../instance/myDB"), ("Thomas", "1.2.3.4", "19/9/2019", "www.google.com"))
# print(lookup("../instance/myDB", "Thomas"))
