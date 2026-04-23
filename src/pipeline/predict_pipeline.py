import sys
import os
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object
import pandas as pd

class PredictPipeline:
    def __init__(self):
        pass

    def reorder_df(self, unordered_df):
        logging.info("Reordering columns of the unordered df.")
        train_df_path = os.path.join('artifacts', 'train.csv')
        train_df = pd.read_csv(train_df_path)
        col_order = [c for c in train_df.columns if c != 'price_cr']
        ordered_df = unordered_df.reindex(columns=col_order).reset_index(drop=True)
        logging.info("Columns have been reordered.")
        return ordered_df
    
    def predict(self, unordered_df):
        logging.info("Prediction started.")

        # user_query_point is an unordered df which can't be read by the model.
        # We need to reorder its features just like the training df.
        ordered_df = self.reorder_df(unordered_df)

        try:
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
            model_path = os.path.join('artifacts', 'model.pkl')

            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)

            df_scaled = preprocessor.transform(ordered_df)
            pred = model.predict(df_scaled)
            logging.info(f"Prediction completed. Price in Cr: {pred[0]}")
            return pred[0]

        except Exception as e:
            logging.info("Exception occurred in prediction")
            raise CustomException(e, sys)