from src.constants import *
from src.config.configuration import *
import os, sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.utils import load_model  # Assuming load_model is a function to load the saved models


class PredictionPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            preprocessor_path = PREPROCESSING_OBJ_FILE
            model_path = MODEL_FILE_PATH
            preprocessor = load_model(preprocessor_path)
            model = load_model(model_path)
            
            processed_features = preprocessor.transform(features)
            predictions = model.predict(processed_features)
            return predictions
        
        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    def __init__(self, 
                 Delivery_person_Age: int,
                 Delivery_person_Ratings: float,
                 weather_conditions: str,
                 Road_traffic_density: str,
                 Vehicle_condition: int,
                 multiple_deliveries: int,
                 distance: float,
                 Type_of_order: str,
                 Type_of_vehicle: str,
                 Festival: str,
                 City: str):
        self.Delivery_person_Age = Delivery_person_Age
        self.Delivery_person_Ratings = Delivery_person_Ratings
        self.weather_conditions = weather_conditions
        self.Road_traffic_density = Road_traffic_density
        self.Vehicle_condition = Vehicle_condition
        self.multiple_deliveries = multiple_deliveries
        self.distance = distance
        self.Type_of_order = Type_of_order
        self.Type_of_vehicle = Type_of_vehicle
        self.Festival = Festival
        self.City = City

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'Delivery_person_Age': [self.Delivery_person_Age],
                'Delivery_person_Ratings': [self.Delivery_person_Ratings],
                'weather_conditions': [self.weather_conditions],
                'Road_traffic_density': [self.Road_traffic_density],
                'Vehicle_condition': [self.Vehicle_condition],
                'multiple_deliveries': [self.multiple_deliveries],
                'distance': [self.distance],
                'Type_of_order': [self.Type_of_order],
                'Type_of_vehicle': [self.Type_of_vehicle],
                'Festival': [self.Festival],
                'City': [self.City]
            }
            
            df = pd.DataFrame(custom_data_input_dict)
            return df

        except Exception as e:
            logging.info(f"Error occurred in prediction pipeline")
            raise CustomException(e, sys)

