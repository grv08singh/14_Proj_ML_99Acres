from flask import Flask, render_template, request
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)

app=application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET','POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
            area_sqm = float(request.form.get('area_sqm')),
            bhk = int(request.form.get('bhk')),
            bathroom = int(request.form.get('bathroom')),
            balcony = int(request.form.get('balcony')),
            addl_room = int(request.form.get('addl_room')),
            sector = int(request.form.get('sector')),
            landmark_count = int(request.form.get('landmark_count')),
            has_hospital_or_clinic = bool(request.form.get('has_hospital_or_clinic')),
            has_police_stn = bool(request.form.get('has_police_stn')),
            has_fire_stn = bool(request.form.get('has_fire_stn')),
            has_mall = bool(request.form.get('has_mall')),
            has_market = bool(request.form.get('has_market')),
            has_park = bool(request.form.get('has_park')),
            has_bank_or_atm = bool(request.form.get('has_bank_or_atm')),
            has_institute = bool(request.form.get('has_institute')),
            has_airport = bool(request.form.get('has_airport')),
            has_rly_stn = bool(request.form.get('has_rly_stn')),
            has_metro_stn = bool(request.form.get('has_metro_stn')),
            has_expy = bool(request.form.get('has_expy')),
            has_petrol_pump = bool(request.form.get('has_petrol_pump')),
            has_hotel = bool(request.form.get('has_hotel')),
            has_temple_or_church = bool(request.form.get('has_temple_or_church')),
            has_famous_chowk = bool(request.form.get('has_famous_chowk')),
            has_club = bool(request.form.get('has_club')),
            has_stadium = bool(request.form.get('has_stadium')),
            has_restro_cafe = bool(request.form.get('has_restro_cafe')),
            area_type = request.form.get('area_type'),
            floor_rise = request.form.get('floor_rise'),
            age = request.form.get('age'),
            society = request.form.get('society'),
            city = request.form.get('city')
        )

        pred_df = data.get_data_as_dataframe()
        print(pred_df)

        predict_pipeline=PredictPipeline()
        results=predict_pipeline.predict(pred_df)
        return render_template("home.html", results=results[0])