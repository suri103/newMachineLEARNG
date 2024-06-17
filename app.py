from src.constants import *
from src.config.configuration import *
import os, sys
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_trainer import ModelTrainer
from flask import Flask
from src.pipeline.prediction_pipeline import CustomData,Predictionpipeline


feature_engineering_file_path = FEATURE_ENGG_OBJ_FILE_PATH
transformer_file_path = PREPROCESING_OBJ_FILE
model_file_path = MODEL_FILE_PATH
UPLOAD_FOLDER = "batch_Prediction/UPLOADED_CSV_FILE"
app = Flask(__name__, template_folder="templates")
ALLOWED_EXTENSION = {'csv'}


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        data = CustomData(
            Delivery_person_Age=int(request.form.get('Delivery_person_Age')),
            Delivery_person_Ratings=float(request.form.get('Delivery_person_Ratings')),
            weather_conditions=request.form.get('weather_conditions'),
            Road_traffic_density=request.form.get('Road_traffic_density'),
            Vehicle_condition=int(request.form.get('Vehicle_condition')),
            multiple_deliveries=int(request.form.get('multiple_deliveries')),
            distance=float(request.form.get('distance')),
            Type_of_order=request.form.get('Type_of_order'),
            Type_of_vehicle=request.form.get('Type_of_vehicle'),
            Festival=request.form.get('Festival'),
            City=request.form.get('City')
        )

        final_new_data = data.get_data_as_dataframe()
        predict_pipeline = Predictionpipeline()
        pred = predict_pipeline.predict(final_new_data)
        result = int(pred[0])
        return render_template('form.html', final_result=result)
    

@app.route('/batch', methods=['GET', 'POST'])
def perform_batch_prediction():
    if request.method == 'GET':
        return render_template('batch.html')
    else:
        file = request.files['csv_file']
        directory_path = UPLOAD_FOLDER
        os.makedirs(directory_path, exist_ok=True)

        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION:
            for filename in os.listdir(os.path.join(UPLOAD_FOLDER)):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)

            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            print(file_path)








