#!/usr/bin/python3
""" Starts a Flash Web Application """
import uuid
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template
app = Flask(__name__)
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/100-hbnb/', strict_slashes=False)
def hbnb():
    """ HBNB is alive! """
    states = storage.all(State)
    states = [state for state in states.values()]

    amenities = storage.all(Amenity)
    amenities = [am for am in amenities.values()]

    places = storage.all(Place)
    places = [place for place in places.values()]

    return render_template('100-hbnb.html',
                           states=states,
                           amenities=amenities,
                           places=places, cache_id=uuid.uuid4())


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
