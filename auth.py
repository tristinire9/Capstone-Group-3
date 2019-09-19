import functools
import sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from normal_db_functions import get_db, init_db

bp = Blueprint('mold', __name__)

@bp.route('/hello')
def hello_world():
    # db = init_db()
    db = get_db()

    # sqlite_insert_query = """INSERT INTO `components`
    #                               ('name', 'version_num', 'date', 'url')
    #                                VALUES
    #                               ('James','1.2.3','2019-03-17','www.baidu.com')"""
    #
    # db.execute(sqlite_insert_query)
    # db.commit()

    # name = "James"
    all_rows = db.execute(
        'SELECT * FROM components'
    ).fetchall()

    rows = ""
    for row in all_rows:
        row = str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "," + str(row[4]) + "; "
        rows = rows + row

    return rows


