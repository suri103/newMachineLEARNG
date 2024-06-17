from src.constants import *
from src.config.configuration import *
import os, sys
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import CustomException
import pickle
from sklearn.pipeline import Pipeline

PREDICTION_FOLDER = "batch_prediction"
PREDICTION_CSV = "prediction.csv"
PREDICTION_FILE = "output.csv"
FEATURE_ENG_FOLDER = "feature_eng"

ROOT_DIR = os.getcwd()
BATCH_PREDICTION = os.path.join(ROOT_DIR, PREDICTION_FOLDER, PREDICTION_CSV)
FEATURE_ENG_PATH = os.path.join(ROOT_DIR, PREDICTION_FOLDER, FEATURE_ENG_FOLDER)

class BatchPrediction:
    def __init__(self, input_file_path, model_file_path, transformer_file_path, feature_engineering_file_path) -> None:
        self.input_file_path = input_file_path
        self.model_file_path = model_file_path
        self.transformer_file_path = transformer_file_path
        self.feature_engineering_file_path = feature_engineering_file_path

    def start_batch_prediction(self):
        try:
            with open(self.feature_engineering_file_path, 'rb') as f:
                feature_pipeline = pickle.load(f)

            with open(self.transformer_file_path, 'rb') as f:
                processor = pickle.load(f)

            model = self.load_model(file_path=self.model_file_path)
        except Exception as e:
            raise CustomException(e, sys)

        feature_engineering_pipeline = Pipeline([('feature_engineering', feature_pipeline)])
        
        df = pd.read_csv(self.input_file_path)
        df.to_csv('df_zomato_delivery_time_prediction.csv')

        df = feature_engineering_pipeline.transform(df)
        df.to_csv('feature_engineering.csv')

        os.makedirs(FEATURE_ENG_PATH, exist_ok=True)
        file_path = os.path.join(FEATURE_ENG_PATH, 'batch_feature_eng.csv')
        df.to_csv(file_path, index=False)

        df = df.drop('time_taken(min)', axis=1)
        df.to_csv('time_taken_dropped.csv')

        transformed_data = processor.transform(df)
        file_path = os.path.join(FEATURE_ENG_PATH, 'processed_data.csv')
        
        predictions = model.predict(transformed_data)
        df_prediction = pd.DataFrame(predictions, columns=['prediction'])

        os.makedirs(PREDICTION_FOLDER, exist_ok=True)
        csv_path = os.path.join(PREDICTION_FOLDER, 'output.csv')

        df_prediction.to_csv(csv_path, index=False)
        logging.info('Batch prediction done')

    def load_model(self, file_path):
        try:
            with open(file_path, 'rb') as model_file:
                model = pickle.load(model_file)
            return model
        except Exception as e:
            raise CustomException(e, sys)

# Example usage:
# batch_predictor = BatchPrediction('input.csv', 'model.pkl', 'transformer.pkl', 'feature_pipeline.pkl')
# batch_predictor.start_batch_prediction()
