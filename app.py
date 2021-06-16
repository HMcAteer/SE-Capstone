#!/usr/bin/env python
import pandas as pd
import gmaps.datasets
import pyrebase
# pyrebase is a module for firebase with python
from flask import Flask, render_template, request, session, url_for, redirect
from ipywidgets.embed import embed_minimal_html
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons

app = Flask(__name__)
app.secret_key = 'secret'
app.config['GOOGLEMAPS_KEY'] = "AIzaSyBIJaHN_KDnQYeREmXcBy-J2Kov5Pxm4N8"
GoogleMaps(app)

firebaseConfig = {
    "apiKey": "AIzaSyC_PlBqGrtGn9dw3O4ZOVtAoEGEShPbbo0",
    "authDomain": "infernoindex-c0659.firebaseapp.com",
    "databaseURL": "https://infernoindex-c0659-default-rtdb.firebaseio.com",
    "projectId": "infernoindex-c0659",
    "storageBucket": "infernoindex-c0659.appspot.com",
    "messagingSenderId": "532288487048",
    "appId": "1:532288487048:web:bb229766cce1ebceb1293d"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# the push function should also assign a random id before writing the values
def writetodb(location, desc):
    db.child("reports").push({"location": location, "desc": desc})


def getreports():
    reports = db.child("reports").get()
    return reports



'''
gmaps.configure(api_key='AIzaSyBIJaHN_KDnQYeREmXcBy-J2Kov5Pxm4N8')
rawdata = pd.read_csv('Current_Wildfire_Points.csv')
cleanData = rawdata[['InitialLatitude', 'InitialLongitude', 'DailyAcres']]
washedData = cleanData.dropna()
locations = washedData[['InitialLatitude', 'InitialLongitude']]
weights = washedData['DailyAcres']
fig = gmaps.figure(map_type='SATELLITE')
fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))
embed_minimal_html('templates/export.html', views=[fig])
'''


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        loc = request.form['location']
        des = request.form['desc']
        writetodb(loc, des)
        reps = getreports()
        all_post = db.child("reports").get().val()
        posts = []
        for i, (key, value) in enumerate(all_post.items()):
            posts.append(value)
            print(value)

        return render_template('userReports.html', reports=posts)
    else:
        return render_template('userReports.html')


@app.route('/map')
def show_fire_map():
    gmaps.configure(api_key='AIzaSyBIJaHN_KDnQYeREmXcBy-J2Kov5Pxm4N8')
    rawdata = pd.read_csv('Current_Wildfire_Points.csv')
    cleanData = rawdata[['InitialLatitude', 'InitialLongitude', 'DailyAcres']]
    washedData = cleanData.dropna()
    lat = washedData['InitialLatitude'].values.tolist()
    long = washedData['InitialLongitude'].values.tolist()

    return render_template("map.html", latList = lat, longList = long )

@app.route('/air')
def show_air_map():
    gmaps.configure(api_key='AIzaSyBIJaHN_KDnQYeREmXcBy-J2Kov5Pxm4N8')
    rawdata = pd.read_csv('air.csv')
    cleanData = rawdata[['SITE_LATITUDE', 'SITE_LONGITUDE']]
    washedData = cleanData.dropna()
    lat = washedData['SITE_LATITUDE'].values.tolist()
    long = washedData['SITE_LONGITUDE'].values.tolist()

    return render_template("air.html", latList=lat, longList=long)


users = []


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
users.append(User(1,'Hugh','bigpapa'))
@app.before_request
def before_request():
    global users
    user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        user = user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return render_template('index.html')
        else:
            return render_template('login.html')

    return render_template('login.html')