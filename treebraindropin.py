from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os
import sqlite3
import braintree

app = Flask(__name__) # create the application instance
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'databasetreebraindropin.db'),
    BRAINTREE_MERCHANT_ID='ryqy4yyw7m5bf92h',
    BRAINTREE_ENVIRONMENT='sandbox',
    BRAINTREE_PUBLIC_KEY='ymtqgy8773zq2fw3', 
    BRAINTREE_PRIVATE_KEY='7dd7253c4c53d675f15e869212659579',
 )) #set config environment variables
# app.config.from_envvar('TREEBRAINDROPIN_SETTINGS', silent=True)

@app.route('/', methods=['GET'])
def get_client_token():
    configure_braintree_gateway()
    client_token = braintree.ClientToken.generate()
    return render_template('checkout.html', client_token=client_token)

@app.route('/store_nonce/', methods=['POST'])
def store_nonce():
    nonce = request.form['nonce']
    nonce_type = request.form['payment_method_type']
    app.logger.info('Nonce: %s', nonce)
    db = get_db()
    db.execute('insert into nonces (nonce) values (?)', [nonce])
    db.commit()
    return url_for('show_nonces')

@app.route('/show_nonces/')
def show_nonces():
    db = get_db()
    query = db.execute('select id, nonce, time from nonces order by time desc')
    all_nonces = query.fetchall()
    app.logger.info('all_nonces: %s', all_nonces)
    return render_template('show_nonces.html', nonce_table=all_nonces)

@app.route('/print_client_token/', methods=['GET'])
def print_client_token():
    configure_braintree_gateway()
    client_token = braintree.ClientToken.generate()
    return client_token
    # to do: add display of decoded client token
    # return render_template('client_token.html', client_token=client_token)


def configure_braintree_gateway():
    """Sets up the Braintree gateway configuration.
    Must be run before any Braintree code.
    """
    braintree.Configuration.configure(
        app.config['BRAINTREE_ENVIRONMENT'],
        merchant_id=app.config['BRAINTREE_MERCHANT_ID'],
        public_key=app.config['BRAINTREE_PUBLIC_KEY'],
        private_key=app.config['BRAINTREE_PRIVATE_KEY']
)

# Database stuff

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
        app.logger.info('%s', g.sqlite_db)
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
    )
# run
#   sqlite3 treebraindropin.db < schema.sql
# before launching for the first time
