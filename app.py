import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


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
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
    )

###Start HERE:
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation for last 12 months"""
    # Query precipitatoin
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    year_precp = session.query(Measurement.date, func.max(Measurement.prcp)).filter(func.strftime('%Y-%m-%d',Measurement.date) > year_ago).group_by(Measurement.date).all()
    all_prcp = []
    for date, prcp in year_precp:
        precp_dict = {}
        precp_dict["date"] = date
        precp_dict["prcp"] = prcp
        all_prcp.append(precp_dict)

    return jsonify(all_prcp)
   

    # Convert list of tuples into normal list
    #year_results = list(np.ravel(year_precp))

    return jsonify(all_prcp)
    session.close()

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Stations"""
    # Query all Stations
    stations = session.query(Station.station, Station.name, Station.elevation, Station.latitude, Station.longitude).all()


    return jsonify(stations)

    session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list temperatures for Station"""
    # Query all temps for last year
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    year_temps = session.query(Measurement.date, Measurement.tobs).filter((Measurement.station)=="USC00519281").filter(func.strftime('%Y-%m-%d',Measurement.date) > year_ago).group_by(Measurement.date).all()


    return jsonify(year_temps)

    session.close()


@app.route("/api/v1.0/<start><br>")
def start():
    session = Session(engine)
    start_date = ''
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter((Measurement.date)>=start_date.all())
    
    return(temps)

    session.close()

@app.route("/api/v1.0/<start>/<end><br>")
def start_end():
    session = Session(engine)
    start_date = ''
    end_date = ''
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter((Measurement.date>=start_date).filter(Measurement.date<= end_date).all())

    return jsonify(temps)

    session.close()
    
   
    if __name__ == '__main__':
        app.run(debug=True)
