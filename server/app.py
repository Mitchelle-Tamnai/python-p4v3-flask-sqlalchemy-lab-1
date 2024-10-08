# server/app.py
#!/usr/bin/env python3

import json
from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route("/earthquakes/<int:id>", methods=["GET"])
def get_earthquake_by_id(id):
    earthquake = db.session.get(Earthquake, id)
    if not earthquake:
        response = make_response(json.dumps({'message': f'Earthquake {id} not found.'}), 404)
        response.mimetype = 'application/json'
        return response
    
    earthquake_data = {
        'id': earthquake.id,
        'location': earthquake.location,
        'magnitude': earthquake.magnitude,
        'year' : int(earthquake.year)
    }
    
    response = make_response(json.dumps(earthquake_data), 200)
    response.mimetype = 'application/json'
    return response


@app.route("/earthquakes/magnitude/<float:magnitude>", methods=["GET"])
def get_earthquakes_by_magnitude(magnitude):
    # Query for earthquakes with magnitude greater than or equal to the specified magnitude
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Create the response dictionary
    response_data = {
        "count": len(earthquakes),
        "quakes": [
            {
                "id": quake.id,
                "location": quake.location,
                "magnitude": quake.magnitude,
                "year": int(quake.year)
            } for quake in earthquakes
        ]
    }
    
    # Create and return the response
    response = make_response(json.dumps(response_data), 200)
    response.mimetype = 'application/json'
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
