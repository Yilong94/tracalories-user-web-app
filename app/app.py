#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, session
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
# from forms import *
import os
import requests

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/qrscanner')
def qrscanner():
    return render_template('qrscanner.html')

@app.route('/menu')
def menu():
    qr = request.args.get('qr')
    r = requests.get(qr)
    items = r.json()
    session['items'] = items
    return render_template('menu.html', items=items)

@app.route('/confirm/<int:id>')
def confirm(id):
    items = session.pop('items', [1,2,3])
    item = items[id-1]
    return render_template('confirmation.html', item=item)

@app.route('/wait')
def wait():
    return render_template('wait.html')

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5023))
    app.run(host='0.0.0.0', port=port)

