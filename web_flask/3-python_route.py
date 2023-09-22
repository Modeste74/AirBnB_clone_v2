#!/usr/bin/python3
"""starts a flask web app"""
from flask import Flask
from markupsafe import escape
"""creates an instance in flask"""
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """returns a display text"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """returns HBNB"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """returns C + text"""
    return f"C {escape(text.replace('_', ' '))}"


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text='is cool'):
    """return python text else python is cool"""
    return f"Python {escape(text.replace('_', ' '))}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
