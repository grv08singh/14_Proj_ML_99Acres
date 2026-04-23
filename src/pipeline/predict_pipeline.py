import sys
import os
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object
from src.utils import reorder_df
import pandas as pd

class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self, unordered_df):
        logging.info("Entering predict method of PredictPipeline class")
        logging.info("Prediction started.")
        try:
            logging.info("Reading model error to set prediction bounds")
            model_error_path = os.path.join("artifacts", "model_error.txt")
            with open(model_error_path, 'r' ) as f:
                model_error = f.read()
            lb = 1 - float(model_error.strip())
            ub = 1 + float(model_error.strip())
            logging.info(f"Model error read successfully. Lower bound: {lb}, Upper bound: {ub}")

        except Exception as e:
            logging.info("Exception occurred in reading error from model_error.txt, setting custom error of 5%")
            alpha = 0.05
            lb = 1 - alpha
            ub = 1 + alpha
            logging.info(f"Error set to 5%. Lower bound: {lb}, Upper bound: {ub}")

        # user_query_point is an unordered df which can't be read by the model.
        # We need to reorder its features just like the training df.
        ordered_df = reorder_df(unordered_df)

        try:
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
            model_path = os.path.join('artifacts', 'pred_model.pkl')

            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)

            df_scaled = preprocessor.transform(ordered_df)
            pred = model.predict(df_scaled)
            price = pred[0]
            price_lower = price * lb
            price_upper = price * ub
            logging.info(f"Prediction completed. Price between: {price_lower} - {price_upper} crore")
            logging.info("Exiting predict method of PredictPipeline class")
            return price_lower, price_upper

        except Exception as e:
            logging.info("Exception occurred in prediction")
            raise CustomException(e, sys)