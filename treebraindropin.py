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


@app.route('/', methods=["GET"])
def get_client_token():
    client_token = braintree.ClientToken.generate()
    return render_template('checkout.html', client_token=client_token)

@app.route('/print_client_token', methods=["GET"])
def print_client_token():
    client_token = braintree.ClientToken.generate()
    return client_token
    # to do: add display of decoded client token
    # return render_template('client_token.html', client_token=client_token)

@app.route('/nonce_received', methods=['POST'])
def store_nonce():
    nonce = request.form["nonce"]
    db = get_db()
    db.execute('insert into nonces (nonce) values (?)', nonce)
    db.commit()
    return nonce
    # to do: add real display of nonce / more stuff
    # return render_template('nonce_received.html', nonce=nonce)

@app.route('/past_nonces')
def show_nonces():
    db = get_db()
    query = db.execute('select pk, nonce, time from nonces order by time asc')


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
