import pickle
import boto3
from datetime import datetime
import pandas as pd
import numpy as np

class TennisModel(object):

    def __init__(self):
        self._model = self.download_latest_model_s3()

    def download_latest_model_s3(self):
        MODEL_FILE = "model.pkl"
        bucket_name = "tennis-prediction"
        s3 = boto3.client('s3')

        # List objects in the bucket
        response = s3.list_objects_v2(Bucket=bucket_name)

        # Find the latest deployment folder
        latest_folder = None
        latest_timestamp = datetime.min
        for obj in response.get('Contents', []):
            key = obj['Key']
            if key.startswith('Deployment_'):
                key = key.split("/")[0]
                timestamp_str = key.split("_")[1]
                timestamp = datetime.strptime(timestamp_str, '%Y%m%d %H%M%S')
                if timestamp > latest_timestamp:
                    latest_timestamp = timestamp
                    latest_folder = key

        if latest_folder:
            # Download model file
            model_file_key = f'{latest_folder}/{MODEL_FILE}'
            s3.download_file(bucket_name, model_file_key, MODEL_FILE)
            print(f"Downloaded latest model from S3: {model_file_key}")

            with open(MODEL_FILE, 'rb') as f:
                model_load = pickle.load(f)  # Adjust this according to your model loading mechanism
                print("Model loaded successfully.")

            return model_load
        else:
            print("No deployment folders found in S3.")
            return None

    def predict(self, X, features_names=None):
        pre_data = {
            'Series': [0],
            'Court': [1],
            'Surface': [3],
            'Player_1': [506],
            'Player_2': [428],
            'Rank_1': [65],
            'Rank_2': [71],
            'Pts_1': [802],
            'Pts_2': [744],
            'Odd_1': X[0],
            'Odd_2': X[1],
        }
        pre_data = pd.DataFrame(pre_data)

        prediction = self._model.predict(pre_data)
        return np.array(prediction)
