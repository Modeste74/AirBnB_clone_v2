#!/usr/bin/python3
# uses storage to fetch data and display a html page
from flask import Flask
from flask import render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def state_list():
    """display a html page"""
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state_details(id):
    states = storage.all(State)
    for state in states.values():
        if state.id == id:
            cities = sorted(state.cities, key=lambda city: city.name)
            return render_template('9-states.html', state=state, cities=cities)
    return render_template('9-states.html')


@app.teardown_appcontext
def teardown(exception):
    """removes currect sqlalchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
