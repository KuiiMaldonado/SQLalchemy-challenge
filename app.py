#Import flask dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
import datetime as dt

#DB path
db_path = "Resources/hawaii.sqlite"

#Creating engine for db
engine = create_engine(f'sqlite:///{db_path}')

#Reflecting existing tables in the database
Base = automap_base()
Base.prepare(engine, reflect=True)

#Creating a class for each key
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask app setup
app = Flask(__name__)


#Defining app routes
@app.route("/")
def home():
    return (f"<h3>Welcome to Climate Analysis API</h3>"
            f"Available routes:</br>"
            f"/api/v1.0/precipitation</br>"
            f"/api/v1.0/stations</br>"
            f"/api/v1.0/tobs</br>"
            f"/api/v1.0/startDate</br>"
            f"/api/v1.0/startDate/endDate</br>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Creating a session for querying the db
    session = Session(bind=engine)

    #Dictionary for returning the data response
    prcp_dict = {}
    prcp_data = session.query(Measurement.date, Measurement.prcp)
    for record in prcp_data:
        prcp_dict[record.date] = record.prcp

    session.close()
    return (jsonify(prcp_dict))

@app.route("/api/v1.0/stations")
def stations():
    #Creating a session for querying the db
    session = Session(bind=engine)

    #Dictionary for returning the data response
    stations_dict = {}
    stations_data = session.query(Station.station, Station.name)
    for record in stations_data:
        stations_dict[record.station] = record.name
    
    session.close()
    return (jsonify(stations_dict))

@app.route("/api/v1.0/tobs")
def tobs():
    #Creating a session for querying the db
    session = Session(bind=engine)

    #Dictionary for returning the data response
    tobs_dict = {}
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= query_date).filter(Measurement.station == 'USC00519281')
    for record in tobs_data:
        tobs_dict[record.date] = record.tobs

    session.close()
    return (jsonify(tobs_dict))

@app.route("/api/v1.0/<startDate>")
def startDateInfo(startDate):
    #Creating a session for querying the db
    session = Session(bind=engine)

    data = session.query(Measurement.date, func.min(Measurement.tobs).label('min_temp'),\
                                                                func.max(Measurement.tobs).label('max_temp'),\
                                                                func.avg(Measurement.tobs).label('avg_temp')).filter(Measurement.date >= startDate)
    #Dictionary for returning the data response
    for record in data:
        data_dict = {"date":record.date,"tmin":record.min_temp, "tmax":record.max_temp, "tavg":record.avg_temp}

    session.close()
    return (jsonify(data_dict))

@app.route("/api/v1.0/<startDate>/<endDate>")
def rangeDateInfo(startDate, endDate):
    #Creating a session for querying the db
    session = Session(bind=engine)

    data = session.query(Measurement.date, func.min(Measurement.tobs).label('min_temp'),\
                                                                func.max(Measurement.tobs).label('max_temp'),\
                                                                func.avg(Measurement.tobs).label('avg_temp')).\
                                                                filter(Measurement.date >= startDate).filter(Measurement.date <= endDate)
    #Dictionary for returning the data response
    for record in data:
        data_dict = {"date":record.date,"tmin":record.min_temp, "tmax":record.max_temp, "tavg":record.avg_temp}

    session.close()
    return (jsonify(data_dict))



if __name__ == "__main__":
    app.run(debug=True)