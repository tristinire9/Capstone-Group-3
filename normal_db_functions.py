import sqlite3


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file, isolation_level=None)
    except sqlite3.Error as e:
        print(e)

    return conn


def create_component(conn, component):
    """
    Create a new component into the components table
    :param conn:
    :param component:
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
def check_duplicate(db_file, fileName, versionNumber):
    conn = sqlite3.connect(db_file, isolation_level=None)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM components WHERE name = ? AND version_num = ?", (fileName, versionNumber))
    data = cursor.fetchall()
    if len(data) == 0:
        return False
    else:
        return True


# return a list containing all components' names
def all_components_names(db_file):
    conn = sqlite3.connect(db_file, isolation_level=None)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM components")
    all_components = cursor.fetchall()

    component_names_list = []

    for component in all_components:
        component_names_list.append(component[1])
    return component_names_list


# return a list containing all the version numbers of a specific component
def lookup(db_file, componentName):
    conn = sqlite3.connect(db_file, isolation_level=None)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM components WHERE name = ? ", (componentName,))
    components = cursor.fetchall()

    versionNumbers = []
    for component in components:
        versionNumbers.append(component[2])

    return versionNumbers



# create_component(create_connection("../instance/myDB"), ("Thomas", "1.2.3.4", "19/9/2019", "www.google.com"))
# print(lookup("../instance/myDB", "Thomas"))