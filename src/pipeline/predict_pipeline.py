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
                    bhk: int,
                    sector: int,
                    floor_rise: str,
                    age: str,
                    has_hospital_or_clinic: bool,
                    has_mall: bool,
                    has_market: bool,
                    has_park: bool,
                    has_bank_or_atm: bool,
                    has_institute: bool,
                    has_airport: bool,
                    has_metro_stn: bool):

        self.bhk = bhk
        self.sector = sector
        self.floor_rise = floor_rise
        self.age = age
        self.has_hospital_or_clinic = has_hospital_or_clinic
        self.has_mall = has_mall
        self.has_market = has_market
        self.has_park = has_park
        self.has_bank_or_atm = has_bank_or_atm
        self.has_institute = has_institute
        self.has_airport = has_airport
        self.has_metro_stn = has_metro_stn


    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "bhk": [self.bhk],
                "sector": [self.sector],
                "floor_rise": [self.floor_rise],
                "age": [self.age],
                "has_hospital_or_clinic": [self.has_hospital_or_clinic],
                "has_mall": [self.has_mall],
                "has_market": [self.has_market],
                "has_park": [self.has_park],
                "has_bank_or_atm": [self.has_bank_or_atm],
                "has_institute": [self.has_institute],
                "has_airport": [self.has_airport],
                "has_metro_stn": [self.has_metro_stn]
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            logging.info("Exception occurred in get_data_as_dataframe method of CustomData class")
            raise CustomException(e, sys)