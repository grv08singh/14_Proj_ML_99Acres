import os
import sys
from src.exception import CustomException
from src.logger import logging

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import dill

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        logging.error("Error occurred while saving object: %s", str(e))
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        logging.error("Error occurred while loading object: %s", str(e))
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}

        for model_name, model in models.items():
            param = params[model_name]

            print(f"\n{model_name}: Applying GridSearchCV with parameters: {param}")
            gs = GridSearchCV(model, param, cv=5)
            gs.fit(X_train, y_train)
            print(f"Best parameters for {model_name}: \n{gs.best_params_}")
            
            print(f"Training {model_name} with best parameters...")
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)
            report[model_name] = test_model_score

        return report

    except Exception as e:
        logging.error("Error occurred during model evaluation: %s", str(e))
        raise CustomException(e, sys)

def reorder_df(unordered_df):
    logging.info("Reordering columns of the unordered df.")
    train_df_path = os.path.join('artifacts', 'train.csv')

    train_df = pd.read_csv(train_df_path)
    col_order = [c for c in train_df.columns if c != 'price_cr']
    ordered_df = unordered_df.reindex(columns=col_order).reset_index(drop=True)

    logging.info("Columns have been reordered.")
    return ordered_df