#Import flask dependencies
from flask import Flask, jsonify


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
    return ("Work in progress")

@app.route("/api/v1.0/stations")
def stations():
    return ("Work in prgress")

@app.route("/api/v1.0/tobs")
def tobs():
    return ("Work in progress")

@app.route("/api/v1.0/<startDate>")
def startDateInfo(startDate):
    return ("Work in progress")

@app.route("/api/v1.0/<startDate>/<endDate>")
def rangeDateInfo(startDate, endDate):
    return ("Work in progress")



if __name__ == "__main__":
    app.run(debug=True)