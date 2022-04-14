# 6D/19090122/Wisnu Yumna Yudhanta
# 6D/19090040/Robby Syah Hidayat
# 6D/19090110/Gusti Robbani
# 6D/19090017/Khaepah

# username = nim
# password = 123

from datetime import datetime
from datetime import date
import os, random, string
from flask import Flask
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import json 
from dateutil import parser

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "19090122.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class users(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20), unique=False)
    token = db.Column(db.String(20), unique=True, nullable=True)

class events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_creator = db.Column(db.String(20))
    event_name = db.Column(db.String(20))
    event_start_time = db.Column(db.Date)
    event_end_time = db.Column(db.Date)
    event_start_lat = db.Column(db.String(20))
    event_finish_lat = db.Column(db.String(20))
    event_start_lng = db.Column(db.String(20))
    event_finish_lng = db.Column(db.String(20))
    create_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.now)

class logs(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    event_name = db.Column(db.String(20))
    log_lat = db.Column(db.String(20))
    log_lng = db.Column(db.String(20))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)

db.create_all()

@app.route("/api/v1/users/create", methods=["POST"])
def create_user():
    username = request.json['username']
    password = request.json['password']

    newUsers = users(username=username, password=password)

    db.session.add(newUsers)
    db.session.commit() 
    return jsonify({
        'msg': 'registrasi sukses'
        })

@app.route("/api/v1/users/login", methods=["POST"])
def login():
    username = request.json['username']
    password = request.json['password']

    user = users.query.filter_by(username=username, password=password).first()

    if user:
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        users.query.filter_by(username=username, password=password).update({'token': token})
        db.session.commit()

        return jsonify({
        'msg': 'login sukses',
        'token': token
        })

    else:
        return jsonify({
        'msg': 'login gagal '
        })

@app.route("/api/v1/events/create", methods=["POST"])
def create_event():
    token = request.json['token']

    token = users.query.filter_by(token=token).first()
    if token:
        event_creator = token.username
        event_name = request.json['event_name']
        event_start_time = request.json['event_start_time']
        event_end_time = request.json['event_end_time']
        event_start_lat = request.json['event_start_lat']
        event_finish_lat = request.json['event_finish_lat']
        event_start_lng = request.json['event_start_lng']
        event_finish_lng = request.json['event_finish_lng']

    event_start_times = datetime.strptime(event_start_time, '%Y-%m-%d %H:%M:%S') 
    event_end_times = datetime.strptime(event_end_time, '%Y-%m-%d %H:%M:%S')

    newEvent = events(event_creator=event_creator, event_name=event_name, event_start_time=event_start_times , event_end_time=event_end_times, event_start_lat=event_start_lat, event_finish_lat=event_finish_lat, event_start_lng=event_start_lng, event_finish_lng=event_finish_lng)

    db.session.add(newEvent)
    db.session.commit() 

    return jsonify({
        'msg': 'membuat event sukses'
        })
    
@app.route("/api/v1/events/log", methods=["POST"])
def event_log():
    token = request.json['token']

    token = users.query.filter_by(token=token).first()
    if token:
        username = token.username
        event_name = request.json['event_name']
        log_lat = request.json['log_lat']
        log_lng = request.json['log_lng']
   
    newLog = logs(username=username, event_name=event_name, log_lat=log_lat, log_lng=log_lng)

    db.session.add(newLog)
    db.session.commit() 

    return jsonify({
        'msg': 'berhasil menambahkan record terbaru'
        })

@app.route("/api/v1/events/logs", methods=["GET"])
def event_logs():
    token = request.json['token']

    token = users.query.filter_by(token=token).first()
    if token:
        username = token.username
        event_name = request.json['event_name']
    
    data_log = logs.query.filter_by(event_name=event_name).all()

    array_books = []
    for book in data_log:
        dict_books = {}
        dict_books.update({"username": book.username, "event_name": book.event_name, "log_lat": book.log_lat, "log_lng": book.log_lng})
        array_books.append(dict_books)
    return jsonify(array_books)

if __name__ == '_main_':
    app.run(debug=True, port=4000)