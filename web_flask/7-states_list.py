#!/usr/bin/python3
"""uses storage to fetch data and display a html page"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def state_list():
    """display a html page"""
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exception):
    """removes currect sqlalchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
