import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import braintree

app = Flask(__name__) # create the application instance
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    BRAINTREE_MERCHANT_ID='ryqy4yyw7m5bf92h'
    BRAINTREE_ENVIRONMENT='sandbox'
    BRAINTREE_PUBLIC_KEY='ymtqgy8773zq2fw3'
    BRAINTREE_PRIVATE_KEY='7dd7253c4c53d675f15e869212659579'
)) #set config environment variables

# Database stuff
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return 

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
