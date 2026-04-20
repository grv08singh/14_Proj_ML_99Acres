import sys
import os
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object
import pandas as pd

class PredictPipeline:
    def __init__(self):
        pass

class CustomData:
    def __init__(self,
                 sector: int,
                 bhk: int,
                 bathroom: int,
                 balcony: int,
                 area_sqm: float,
                 society: str,
                 near_hospital: bool,
                 near_school: bool,
                 near_market: bool,
                 near_park: bool,
                 near_mall: bool,
                 near_petrol_pump: bool,
                 near_temple_or_church: bool,
                 near_bank_or_atm: bool,
                 near_institute: bool,
                 near_metro: bool,
                 near_rly_stn: bool,
                 near_airport: bool,
                 near_restaurant_or_cafe: bool,
                 near_club: bool):

        self.sector = sector
        self.bhk = bhk
        self.bathroom = bathroom
        self.balcony = balcony
        self.area_sqm = area_sqm
        self.society = society
        self.near_hospital = near_hospital
        self.near_school = near_school
        self.near_market = near_market
        self.near_park = near_park
        self.near_mall = near_mall
        self.near_petrol_pump = near_petrol_pump
        self.near_temple_or_church = near_temple_or_church
        self.near_bank_or_atm = near_bank_or_atm
        self.near_institute = near_institute
        self.near_metro = near_metro
        self.near_rly_stn = near_rly_stn
        self.near_airport = near_airport
        self.near_restaurant_or_cafe = near_restaurant_or_cafe
        self.near_club = near_club


    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "area_type": [self.area_type],
                "availability": [self.availability],
                "location": [self.location],
                "society": [self.society],
                "size": [self.size],
                "total_sqft": [self.total_sqft],
                "bath": [self.bath],
                "balcony": [self.balcony],
                "price": [self.price]
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            logging.info("Exception occurred in get_data_as_dataframe method of CustomData class")
            raise CustomException(e, sys)