import os
import shutil
import pandas as pd
import opendatasets as od

from aws_logger import logger
from config import DATASET_FILE, data_dir


DATASET_NAME = "atp-tennis-2000-2023daily-pull"
DATASET_LINK = f"https://www.kaggle.com/datasets/dissfya/{DATASET_NAME}"


def data_pull():
    # Pull data from Kaggle
    od.download(DATASET_LINK)
    logger.info("File download successfully")

    # Read file
    filepath = os.path.join(DATASET_NAME, DATASET_FILE)
    if os.path.exists(filepath):
        data = pd.read_csv(filepath)

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # copy data to data folder
        shutil.copy(filepath, data_dir)

        # delete download file
        os.remove(filepath)
        os.rmdir(DATASET_NAME)

    else:
        logger.error("Error: File download failed")
        return None


if __name__ == "__main__":
    data_pull()