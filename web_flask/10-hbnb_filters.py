#!/usr/bin/python3
"""uses storage to fetch data and display a html page"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """displays a page with a popover
    that scroll down while reflecting
    data from storage"""
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    amt = sorted(storage.all(Amenity).values(), key=lambda amt: amt.name)
    return render_template('10-hbnb_filters.html', states=states, amt=amt)


@app.teardown_appcontext
def teardown(exception):
    """removes currect sqlalchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
