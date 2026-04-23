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

from sklearn.neighbors import NearestNeighbors

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "pred_model.pkl")
    trained_model_error_path: str = os.path.join("artifacts", "pred_model_error.txt")
    recommendation_model_file_path: str = os.path.join("artifacts", "recommendation_model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        logging.info("Entered the initiate_model_trainer method of ModelTrainer class")
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
                    'n_estimators': [8,16,32,64,100,128,256],
                    'max_depth': [None, 5, 10, 20]
                },
                "SVR":{
                    'C': [0.1, 10, 70],
                    'epsilon': [0.01, 0.1, 0.14],
                    'gamma': ['scale', 'auto', 0.06],
                    'kernel': ['rbf']
                },
                "Gradient Boosting":{
                    'learning_rate':[0.1,0.01,0.05],
                    'subsample':[0.6,0.8,1],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "AdaBoost":{},
                "XGB":{},
                "CatBoost":{}
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
            r2 = r2_score(y_test, predicted)

            model_error = 1 - r2
            with open(self.model_trainer_config.trained_model_error_path, 'w') as f:
                f.write(str(model_error))

            logging.info(f"Model error saved at: {self.model_trainer_config.trained_model_error_path}")

            logging.info("Model training completed successfully")
            logging.info("Exiting successfully the initiate_model_trainer method of ModelTrainer class")
            return r2

        except Exception as e:
            logging.error("Error occurred during model training: %s", str(e))
            raise CustomException(e, sys)


    def initiate_recommendation_trainer(self, train_array, test_array):
        logging.info("Entered the recommend_more method of ModelTrainer class")
        try:
            logging.info("Splitting training and testing input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )



    df = pd.read_csv("artifacts/data.csv")
    
    # Select features for KNN
    features = ['bedroom', 'area_sqm', 'price_cr']
    
    # Prepare data
    X = df[features].copy()
    user_features = user_query_df[['bedroom', 'area_sqm']].copy()
    user_features['price_cr'] = 0  # Placeholder
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    user_scaled = scaler.transform(user_features)
    
    # KNN model
    knn = NearestNeighbors(n_neighbors=3, metric='euclidean')
    knn.fit(X_scaled)
    
    # Find similar properties
    distances, indices = knn.kneighbors(user_scaled)




            # Using Random Forest for recommendation system
            knn_model = RandomForestRegressor(n_estimators=100, random_state=42)
            knn_model.fit(X_train, y_train)

            save_object(
                file_path=self.model_trainer_config.recommendation_model_file_path,
                obj=rf_model
            )

            logging.info("Recommendation model saved successfully")
            logging.info("Exiting successfully the recommend_more method of ModelTrainer class")
            return rf_model

        except Exception as e:
            logging.error("Error occurred while saving recommendation model: %s", str(e))
            raise CustomException(e, sys
