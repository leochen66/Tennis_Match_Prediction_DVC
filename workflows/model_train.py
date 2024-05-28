import os
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import boto3
import shutil
from config import *
import json
from datetime import datetime

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

from config import MODEL_FILE, REPORT_FILE, IMPORTANCE_PLOT_FILE
from aws_logger import logger


def train(x: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    rf_classifier = RandomForestClassifier(n_estimators=1500, random_state=100, max_depth=6)
    rf_classifier.fit(x, y)
    logger.info("Model train successfully")

    return rf_classifier


def evaluation(model: RandomForestClassifier, x_test: pd.DataFrame, y_test: pd.Series) -> float:

    # Test on testing data and generate report
    y_pred = model.predict(x_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    accuracy = float(accuracy_score(y_test, y_pred))
    logger.info(f"Accuracy: {accuracy}")

    summary_report = {
        "accuracy": accuracy,
        "macro avg": {
            "precision": report["macro avg"]["precision"],
            "recall": report["macro avg"]["recall"],
            "f1-score": report["macro avg"]["f1-score"]
        }
    }

    # Save report as JSON
    with open(REPORT_FILE, 'w') as f:
        json.dump(summary_report, f, indent=4)

    # Save feature importance plot
    feature_importances = model.feature_importances_
    features = ['Series', 'Court', 'Surface', 'Player_1', 'Player_2', 'Rank_1', 'Rank_2', 'Pts_1', 'Pts_2', 'Odd_1', 'Odd_2']
    importance_df = pd.DataFrame({'Feature': features, 'Importance': feature_importances})
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    plt.figure(figsize=(6, 4))
    plt.barh(importance_df['Feature'], importance_df['Importance'])
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.title('Feature Importance')
    plt.savefig(IMPORTANCE_PLOT_FILE)
    plt.close()

    # save model to local
    with open(MODEL_FILE, 'wb') as f:
        rf_classifier_loaded = pickle.dump(model, f)
        logger.info("Model saved in local")

    # Upload artifacts to AWS S3
    s3 = boto3.client('s3')
    timestamp = datetime.now().strftime('%Y%m%d %H%M%S')
    s3_folder_name = f'Deployment_{timestamp}'
    bucket_name = 'tennis-prediction'

    # upload file to S3
    for file_name in [MODEL_FILE, REPORT_FILE, IMPORTANCE_PLOT_FILE]:
        local_file_path = file_name

        s3_file_path = f'{s3_folder_name}/{file_name}'

        s3.upload_file(local_file_path, bucket_name, s3_file_path)
    logger.info(f"Artifacts upload to S3 folder: {s3_folder_name}")

    # delete artifact files
    for file_name in [MODEL_FILE, REPORT_FILE, IMPORTANCE_PLOT_FILE]:
        shutil.copy(file_name, artifact_dir)
        if os.path.exists(file_name):
            os.remove(file_name)

    return accuracy


def get_data(filepath) -> (pd.DataFrame, pd.Series):
    data_df = pd.read_csv(filepath)

    features = ['Series', 'Court', 'Surface', 'Player_1', 'Player_2', 'Rank_1', 'Rank_2', 'Pts_1', 'Pts_2', 'Odd_1', 'Odd_2']
    x = data_df[features]
    y = data_df['Label']

    return x, y


if __name__ == "__main__":
    train_filepath = os.path.join(data_dir, TRAIN_DATA_FILE)
    test_filepath = os.path.join(data_dir, TEST_DATA_FILE)

    x_train, y_train = get_data(train_filepath)
    x_test, y_test = get_data(test_filepath)

    model = train(x_train, y_train)
    evaluation(model, x_test, y_test)