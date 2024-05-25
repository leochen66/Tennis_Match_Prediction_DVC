import os
import pandas as pd
import opendatasets as od

from aws_logger import logger
from config import DATASET_FILE


DATASET_NAME = "atp-tennis-2000-2023daily-pull"
DATASET_LINK = f"https://www.kaggle.com/datasets/dissfya/{DATASET_NAME}"


def data_pull() -> pd.DataFrame:
    # Pull data from Kaggle
    od.download(DATASET_LINK)
    logger.info("File download successfully")

    # Read file
    filepath = os.path.join(DATASET_NAME, DATASET_FILE)
    if os.path.exists(filepath):
        data = pd.read_csv(filepath)

        # delete download file
        os.remove(filepath)
        os.rmdir(DATASET_NAME)

        return data
    else:
        logger.error("Error: File download failed")
        return None
