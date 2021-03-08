import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# flask setup
app = Flask(__name__)

# Flask route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of preciptation by date."""

    # Calculate the date one year from the last date in data set.
    months12_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    last_12_months = session.query(measurement.date, measurement.prcp).\
                        filter(measurement.date > months12_ago).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    prcp_list = []
    for date, prcp in last_12_months:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)
       

@app.route("/api/v1.0/stations")
def stations():
    """List all stations."""
#      # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    stations_query = session.query(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations_query))

    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    """Dates and temp observations for most activate station over the laster year."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    months12_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
# Perform a query to retrieve the data and precipitation scores
    last_12_tobs = session.query(measurement.station, measurement.date, measurement.tobs).\
                        filter(measurement.date > months12_ago).\
                        filter(measurement.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(last_12_tobs))

    return jsonify(tobs_list)
    


@app.route("/api/v1.0/<start>")
def start(start = None):
    """Return a JSON dict of the minimum temperature, the average temperature, and the max temperature for all dates greater than and equal to the start date..
    
    TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start(string): A date string in the format %Y-%m-%d
        
        
    Returns:
        TMIN, TAVG, and TMAX
    """
    # Create our session (link) from Python to the DB
    session = Session(engine)

    min_max_avg = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    
    start_dict = {}
    start_dict["TMIN"] = min_max_avg[0][0]
    start_dict["TAVG"] = min_max_avg[0][1]
    start_dict["TMAX"] = min_max_avg[0][2]
    
    session.close()
    

    return(jsonify(start_dict))

@app.route("/api/v1.0/<start>/<end>")
def startend(start = None, end = None):
    """Return a JSON dict of the minimum temperature, the average temperature, and the max temperature for dates between the start and end date inclusive...
    
    TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start(string): A date string in the format %Y-%m-%d
        end(string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVG, and TMAX
    """
    # Create our session (link) from Python to the DB
    session = Session(engine)

    min_max_avg = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    start_dict = {}
    start_dict["TMIN"] = min_max_avg[0][0]
    start_dict["TAVG"] = min_max_avg[0][1]
    start_dict["TMAX"] = min_max_avg[0][2]
    
    session.close()
    

    return(jsonify(start_dict))



if __name__ == '__main__':
    app.run(debug=True)