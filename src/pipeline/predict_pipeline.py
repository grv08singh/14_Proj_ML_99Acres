import sys
import os
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object
import pandas as pd

class PredictPipeline:
    def __init__(self):
        pass

def predict(self, features):
    try:
        preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
        model_path = os.path.join('artifacts', 'model.pkl')

        preprocessor = load_object(preprocessor_path)
        model = load_object(model_path)

        data_scaled = preprocessor.transform(features)
        pred = model.predict(data_scaled)
        return pred

    except Exception as e:
        logging.info("Exception occurred in prediction")
        raise CustomException(e, sys)

class CustomData:
    def __init__(self,
                    area_sqm: float,
                    bhk: int,
                    bathroom: int,
                    balcony: int,
                    addl_room: int,
                    sector: int,
                    landmark_count: int,
                    has_hospital_or_clinic: bool,
                    has_police_stn: bool,
                    has_fire_stn: bool,
                    has_mall: bool,
                    has_market: bool,
                    has_park: bool,
                    has_bank_or_atm: bool,
                    has_institute: bool,
                    has_airport: bool,
                    has_rly_stn: bool,
                    has_metro_stn: bool,
                    has_expy: bool,
                    has_petrol_pump: bool,
                    has_hotel: bool,
                    has_temple_or_church: bool,
                    has_famous_chowk: bool,
                    has_club: bool,
                    has_stadium: bool,
                    has_restro_cafe: bool,
                    area_type: bool,
                    floor_rise: str,
                    age: str,
                    society: str,
                    city: str):

        self.area_sqm = area_sqm
        self.bhk = bhk
        self.bathroom = bathroom
        self.balcony = balcony
        self.addl_room = addl_room
        self.sector = sector
        self.landmark_count = landmark_count
        self.has_hospital_or_clinic = has_hospital_or_clinic
        self.has_police_stn = has_police_stn
        self.has_fire_stn = has_fire_stn
        self.has_mall = has_mall
        self.has_market = has_market
        self.has_park = has_park
        self.has_bank_or_atm = has_bank_or_atm
        self.has_institute = has_institute
        self.has_airport = has_airport
        self.has_rly_stn = has_rly_stn
        self.has_metro_stn = has_metro_stn
        self.has_expy = has_expy
        self.has_petrol_pump = has_petrol_pump
        self.has_hotel = has_hotel
        self.has_temple_or_church = has_temple_or_church
        self.has_famous_chowk = has_famous_chowk
        self.has_club = has_club
        self.has_stadium = has_stadium
        self.has_restro_cafe = has_restro_cafe
        self.area_type = area_type
        self.floor_rise = floor_rise
        self.age = age
        self.society = society
        self.city = city


    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "area_sqm": [self.area_sqm],
                "bhk": [self.bhk],
                "bathroom": [self.bathroom],
                "balcony": [self.balcony],
                "addl_room": [self.addl_room],
                "sector": [self.sector],
                "landmark_count": [self.landmark_count],
                "has_hospital_or_clinic": [self.has_hospital_or_clinic],
                "has_police_stn": [self.has_police_stn],
                "has_fire_stn": [self.has_fire_stn],
                "has_mall": [self.has_mall],
                "has_market": [self.has_market],
                "has_park": [self.has_park],
                "has_bank_or_atm": [self.has_bank_or_atm],
                "has_institute": [self.has_institute],
                "has_airport": [self.has_airport],
                "has_rly_stn": [self.has_rly_stn],
                "has_metro_stn": [self.has_metro_stn],
                "has_expy": [self.has_expy],
                "has_petrol_pump": [self.has_petrol_pump],
                "has_hotel": [self.has_hotel],
                "has_temple_or_church": [self.has_temple_or_church],
                "has_famous_chowk": [self.has_famous_chowk],
                "has_club": [self.has_club],
                "has_stadium": [self.has_stadium],
                "has_restro_cafe": [self.has_restro_cafe],
                "area_type": [self.area_type],
                "floor_rise": [self.floor_rise],
                "age": [self.age],
                "society": [self.society],
                "city": [self.city]
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            logging.info("Exception occurred in get_data_as_dataframe method of CustomData class")
            raise CustomException(e, sys)