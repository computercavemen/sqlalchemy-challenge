import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

#################################################
# Flask Setup
#################################################

# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station
  
# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
#################################################
# Flask Routes
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        "input start date on penultimate and start and end date between slashes on last as yyyy-mm-dd"

    )

@app.route("/api/v1.0/precipitation")
def date():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    year_from = dt.date(2017,8,23) - dt.timedelta(days = 365)

    # Query 
    results = session.query(measurement.date, measurement.prcp). \
            filter(measurement.date >= year_from).all()

    session.close()

    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query 
    station_list = session.query(station.station).all() # how come station.station doesn't work? 

    session.close()

    station_json = list(np.ravel(station_list))

    return jsonify(station_json)

@app.route("/api/v1.0/tobs")
def tobs():

# Create our session (link) from Python to the DB
    session = Session(engine)

    year_from1 = dt.date(2017,8,18) - dt.timedelta(days = 365)

# Query 
    most_active = session.query(measurement.date, measurement.tobs). \
               filter(measurement.date >= year_from1). \
               filter(measurement.station == 'USC00519281').all()

    session.close()

    active_json = list(np.ravel(most_active))

    return jsonify(active_json)

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    
    start_date = session.query(func.min(measurement.tobs), 
                 func.max(measurement.tobs), 
                 func.avg(measurement.tobs)).\
                 filter(measurement.date >= start).all()

    session.close()

    start_json = list(np.ravel(start_date))
    
    return jsonify(start_json)
    

@app.route("/api/v1.0/<start>/<end>")
def startend_date(start, end):
    session = Session(engine)
    
    startend_date = session.query(func.min(measurement.tobs), 
                 func.max(measurement.tobs), 
                 func.avg(measurement.tobs)).\
                 filter(measurement.date >= start).\
                 filter(end >= measurement.date).all()

    session.close()

    startend_json = list(np.ravel(startend_date))
    
    return jsonify(startend_json)


if __name__ == "__main__":
    app.run(debug=True)