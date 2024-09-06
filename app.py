# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of precipitation dictionary."""
    session = Session(engine)
    Yr_prior = '2016-08-23'
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= Yr_prior).all()
    session.close()

    Recent_yr_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        Recent_yr_precipitation.append(precipitation_dict)

    return jsonify(Recent_yr_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    Station_list = []
    for station in results:
        station_dict = {}
        station_dict["station"] = station[0]
        Station_list.append(station_dict)

    return jsonify(Station_list)
    
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    Yr_prior = '2016-08-23'
    Most_active_station = 'USC00519281'
    results = session.query(Measurement.tobs).filter(Measurement.station == Most_active_station).filter(Measurement.date >= Yr_prior).all()
    session.close()

    tobs_list = []
    for tobs in results:
        tobs_dict = {}
        tobs_dict["tobs"] = tobs[0]
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_stats(start=None, end=None):
    session = Session(engine)
    
    session.close()








if __name__ == "__main__":
    app.run(debug=True)