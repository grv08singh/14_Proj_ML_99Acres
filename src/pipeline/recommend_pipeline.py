import sys
import os
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object
from src.utils import reorder_df
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


class RecommendationPipeline:
    def __init__(self):
        pass

    def get_similar_records(self, unordered_df, n_recommendations=5):
        logging.info("get_similar_records method of RecommendationPipeline class initiated.")  

        try:      
            
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
            preprocessor = load_object(preprocessor_path)

            X_train_path = os.path.join('artifacts', 'data.csv')
            X_train = pd.read_csv(X_train_path)
            X_train = X_train.drop(columns=['price_cr'])
            X_train_scaled = preprocessor.transform(X_train)

            # user_query_point is an unordered df which can't be read by the model.
            # We need to reorder its features just like the training df.
            ordered_df = reorder_df(unordered_df)
            df_scaled = preprocessor.transform(ordered_df)

            #calculating cosine similarity
            similarities = cosine_similarity(df_scaled, X_train_scaled)[0]
            sorted_indices = np.argsort(similarities)[::-1]
            count = 0
            alrdy_society = []
            top_indices = []
            while count < n_recommendations:
                for index in sorted_indices:
                    if X_train.loc[index, 'society'] not in alrdy_society:
                        top_indices.append(index)
                        alrdy_society.append(X_train.loc[index, 'society'])
                        count += 1
                        break
            cosine_similar = X_train.iloc[top_indices].copy()

            #calculating KNN similarity
            model = NearestNeighbors(n_neighbors=n_recommendations, algorithm='ball_tree')
            model.fit(X_train_scaled)
            _, indices = model.kneighbors(df_scaled)
            knn_similar = X_train.iloc[indices[0]].copy()

            logging.info("get_similar_records method of RecommendationPipeline class completed.")
            return cosine_similar, knn_similar

        except Exception as e:
            logging.info("Exception occurred in get_similar_records.")
            raise CustomException(e, sys)
        