#!/usr/bin/python3
from flask import Flask
"""creates an instance of flask"""
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """return a display string"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
