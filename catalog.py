import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from astropy.coordinates import *
import sys
from astroquery.simbad import Simbad
from subprocess import *
from flask import Flask
from flask import request, redirect, render_template
from call import create #change import call to "from call.py import create"
from Visibility import plot, vis
from SED import gen
from helper import *

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #attempts to prevent caching


@app.route('/home') #if home if spressed, render home template
def home():
    return render_template("home.html")

@app.route('/about') #"about us" page
def about_page():
    return render_template("about.html")

@app.route('/resources') #resources page
def resources_page():
    return render_template("resources.html")

#@app.route("/test2", methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def server():

    if request.method == "POST":

        req = request.form


        objects = req.get("Objects") #get list of objects from 
        mode = req["Mode"]
        offset = request.form["Offset"]
        date = req.get("Date")


        create(objects,mode,offset) #create catalog.txt
        plot(date,objects) #create airmass.png
        gen(objects) #create a SED plot for each object (<object_name>_sed.png)

        table = txt_to_df('static/data/catalog.txt') #generate a Pandas DataFrame from the table in catalog.txt
        
        print(table)
        
        vis(date,objects,table) #create visibility.txt
        visib = txt_to_df('static/data/visibility.txt') #generate a Pandas DataFrame from the table in visibility.txt
        
        print(visib)
        
        obj_list=list(objects.split(","))
        return render_template("log.html", t1=table.to_html(index=False), t2=visib.to_html(index=False), obj_list=obj_list, len=len(obj_list))

    else:
        return render_template("home.html")

if __name__ == "__main__":
    app.run()
