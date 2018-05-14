#Dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Boilerplate

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurements = Base.classes.measurements_table
Stations = Base.classes.stations_table
session = Session(engine)

#Start flask app

app = Flask(__name__)


@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurements.tobs).\
        filter(Measurements.date > '2016-05-14')
    last_year_temps_and_dates = list(results)

    return jsonify(last_year_temps_and_dates)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all Stations
    results = session.query(Stations.station).all()
    all_stations = list(results)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperatures():
    results = session.query(Measurements.tobs).\
        filter(Measurements.date > '2016-05-14')
    last_year_temps = list(results)

    return jsonify(last_year_temps)

@app.route("/api/v1.0/<start>")
def start(start):
    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date > start)
    start_date_temps_statistics = list(results)

    return jsonify(start_date_temps_statistics)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date > start).\
        filter(Measurements.date < end)
    startend_date_temps_statistics = list(results)

    return jsonify(startend_date_temps_statistics)


if __name__ == '__main__':
    app.run(debug=True)
