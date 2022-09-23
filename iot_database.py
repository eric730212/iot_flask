from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///iots.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Iots(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    temperature = db.Column('temperature', db.String(100))
    humidity = db.Column('humidity', db.String(100))
    lux = db.Column('lux', db.String(100))
    tvoc = db.Column('tvoc', db.String(100))
    co2 = db.Column('co2', db.String(100))
    pm25 = db.Column('pm25', db.String(100))
    time = db.Column('time', db.String(100))
    def __init__(self, temperature, humidity, lux, tvoc, co2, pm25, time):
        self.temperature = temperature
        self.humidity = humidity
        self.lux = lux
        self.tvoc = tvoc
        self.co2 = co2
        self.pm25 = pm25
        self.time = time

if __name__ =="__main__":
    db.create_all()
    app.run(debug=True)