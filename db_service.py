import sqlite3
from flask import g
from datetime import datetime

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('recipes.db', check_same_thread=False)
        g.c = g.db.cursor()
        g.c.execute('''CREATE TABLE IF NOT EXISTS favorites (id INTEGER PRIMARY KEY, recipe_text TEXT, rating INTEGER, timestamp INTEGER)''')
    return g.db, g.c

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%m/%d/%Y') if timestamp else 'N/A'