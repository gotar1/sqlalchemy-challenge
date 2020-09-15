# import needed modeules...
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

# create an engine and connection setup..reflect ...
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# re-define our tables to python...
Measurement = Base.classes.measurement
Station = Base.classes.station

## Flask Setup
app = Flask(__name__)

## flask routes
@app.route('/')
def welcome():
    """List all available routes"""
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    ## create our session
    session = Session(engine)

    # query database for needed information
    """ Return a json dictionary of dates and precipitation from Measurement database"""
    results = session.query(Measurement.prcp, Measurement.date).all()
    session.close()

    # create the list and then iterate over our query to return needed values....
    all_precipitation = []
    for prcp, date in results:
        precipitation_dict = {"date": "prcp"}
        precipitation_dict['prcp'] = prcp
        precipitation_dict['date'] = date
        all_precipitation.append(precipitation_dict)    
    return jsonify(all_precipitation)

@app.route('/api/v1.0/stations')
def station():
    session = Session(engine)

    """ Return a json list of stations in Station database"""

    station_result = session.query(Station.station).all()
    session.close()

    # create the list and then iterate over our query to return needed values....
    station_list = []
    for stn in station_result:
        if stn not in station_list:
            station_list.append(stn)
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)

    """ Return a json list of temperature observation (tobs) of the most active ststion for the last year"""
    """ Most active station is station number USC00519281..this is from the first part of the hw"""

    tobs_result = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date <= '2017-08-23', Measurement.date >= '2016-08-23').all()
    session.close()

    # create the list and then iterate over our query to return needed values....
    tobs_list = []
    for tob in tobs_result:
        tobs_list.append(tob)
    return jsonify(tobs_list)

@app.route('/api/v1.0/start')
def start():
    session = Session(engine)

    """ Return a json list of the minimum, maximum and average temperature for a given start date"""
    """Prompt user to input a start date for his trip"""
    """Date entry format is: YY-MM-DD"""

    start_date = input('Please Input your Start Date: ')  

     # query database for needed information
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    start_results = session.query(*sel).\
        filter(Measurement.date >= start_date).all()
    session.close()

    # create the list and then iterate over our query to return needed values....
    start_list = []
    for res in start_results:
        start_list.append(res)
    return jsonify(start_list)


@app.route('/api/v1.0/startend')
def startend():
    session = Session(engine)

    """ Return a json list of the minimum, maximum and average temperature for a given start-end date range"""
    """Prompt user to input a start and end date for his trip, Date entry format is: YY-MM-DD"""

    # Date entry format is: YY-MM-DD 
    start_date = input('Please Input your Start Date: ') 
    end_date =  input('Please Input your End Date: ')  

     # query database for needed information
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    start_results = session.query(*sel).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    session.close()

    # create the list and then iterate over our query to return needed values....
    start_list = []
    for res in start_results:
        start_list.append(res)
    return jsonify(start_list)


if __name__ == '__main__':
    app.run(debug=True)
