import functools
import sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db, init_db

bp = Blueprint('mold', __name__)

@bp.route('/hello')
def hello_world():
    db = init_db()

    sqlite_insert_query = """INSERT INTO `components`
                                  ('name', 'version_num', 'date', 'url')
                                   VALUES
                                  ('James','1.2.3','2019-03-17','www.baidu.com')"""

    db.execute(sqlite_insert_query)
    db.commit()

    name = "James"
    one_row = db.execute(
        'SELECT name FROM components WHERE name = ?', (name,)
    ).fetchone()

    return one_row[0]


