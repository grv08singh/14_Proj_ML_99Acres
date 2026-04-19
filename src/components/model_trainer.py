import os
import sys
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models
from dataclasses import dataclass

from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and testing input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                "Linear Regression": LinearRegression(),
                "KNN": KNeighborsRegressor(),
                "Random Forest": RandomForestRegressor(),
                "SVR": SVR(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "AdaBoost": AdaBoostRegressor(),
                "XGB": XGBRegressor(),
                "CatBoost": CatBoostRegressor(verbose=False),
            }
            params={
                "Linear Regression":{},
                "KNN":{
                    'n_neighbors': [3, 5, 7],
                    'weights': ['uniform', 'distance'],
                    'metric': ['euclidean', 'manhattan']
                },
                "Random Forest":{
                    'n_estimators': [8,16,32,64,128,256],
                    'max_depth': [None, 5, 10, 20]
                },
                "SVR":{
                    'C': [0.1, 10, 70],
                    'epsilon': [0.01, 0.14],
                    'gamma': ['scale', 'auto', 0.06],
                    'kernel': ['rbf']
                },
                "Gradient Boosting":{
                    'learning_rate':[.1,.01,.05],
                    'subsample':[0.6,0.7,0.8,0.9],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "AdaBoost":{
                    'learning_rate':[.1,.01,0.05],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "XGB":{
                    'learning_rate':[.1,.01,.05],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoost":{
                    'depth': [None,6,8,10],
                    'learning_rate': [None,0.01, 0.05, 0.1],
                    'iterations': [None,30, 50, 100]
                }
            }

            model_report:dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models, params=params)

            best_model_score = max(model_report.values())
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found with R2 score above 0.6", sys)

            logging.info(f"Best model found: {best_model_name} with R2 score: {best_model_score}")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            return r2_square

        except Exception as e:
            logging.error("Error occurred during model training: %s", str(e))
            raise CustomException(e, sys)