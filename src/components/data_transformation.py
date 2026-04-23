import sys
import os
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import save_object

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation. It performs the following steps:
        1. Define numerical and categorical columns.
        2. Create pipelines for numerical and categorical features.
        3. Combine the pipelines using ColumnTransformer.
        4. Return the preprocessor object.
        '''
        try:
            numerical_columns = ['area_sqm','bedroom','bathroom','balcony','addl_room','landmark_count','has_hospital_or_clinic','has_police_stn','has_fire_stn','has_mall','has_market','has_park','has_bank_or_atm','has_institute','has_airport','has_rly_stn','has_metro_stn','has_expy','has_petrol_pump','has_hotel','has_temple_or_church','has_famous_chowk','has_club','has_stadium','has_restro_cafe']
            categorical_columns = ['area_type','sector','floor_rise','age','society','city']

            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])

            cat_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('ordinal_encoder', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)),
                ('scaler', StandardScaler(with_mean=False))
            ])

            logging.info("Numerical columns standard scaling completed.")
            logging.info("Categorical columns encoding completed.")

            preprocessor = ColumnTransformer(
                transformers=[
                    ('num_pipeline', num_pipeline, numerical_columns),
                    ('cat_pipeline', cat_pipeline, categorical_columns)
                ]
            )
            return preprocessor

        except Exception as e:
            logging.error("Error occurred in get_data_transformer_object: %s", str(e))
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed.")
            logging.info("Obtaining preprocessing object.")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = 'price_cr'

            input_feature_train_df = train_df.drop(columns=[target_column_name])
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name])
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on training and testing dataframe.")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )


            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            logging.error("Error occurred in initiate_data_transformation: %s", str(e))
            raise CustomException(e, sys)