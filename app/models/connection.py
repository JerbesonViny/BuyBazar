import sqlite3
from app import app
from flask import g

DATABASE = './db/bazar.db'

def get_db():
  db = getattr(g, '_database', None)
  
  if db is None:
    g._database = sqlite3.connect(DATABASE)
    db = g._database
  
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  
  if db is not None:
    db.close()