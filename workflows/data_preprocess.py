import pandas as pd
from sklearn.model_selection import train_test_split
import typing
from config import *

from aws_logger import logger


def data_preprocessing() -> pd.DataFrame:

    filepath = os.path.join(data_dir, DATASET_FILE)
    matches_df = pd.read_csv(filepath)

    # remove useless column
    matches_df = matches_df.drop(["Tournament", "Date", "Round", "Best of", "Score"], axis=1)

    # drop row with invalid value
    matches_df = matches_df[(matches_df["Pts_1"] != -1) & 
                            (matches_df["Pts_2"] != -1) & 
                            (matches_df["Odd_1"] != -1) & 
                            (matches_df["Odd_2"] != -1)]

    # create label
    matches_df["Label"] = (matches_df["Winner"] == matches_df["Player_1"]).astype("int")

    # convert categorical columns to numeric codes
    cat_columns = ["Player_1", "Player_2", "Series", "Court", "Surface"]
    for col in cat_columns:
        matches_df[col] = matches_df[col].astype("category").cat.codes

    features = ['Series', 'Court', 'Surface', 'Player_1', 'Player_2', 'Rank_1', 'Rank_2', 'Pts_1', 'Pts_2', 'Odd_1', 'Odd_2', 'Label']
    data_df = matches_df[features]

    return data_df


def data_split(data_df: pd.DataFrame):
    train_df, test_df = train_test_split(data_df, test_size=0.2, random_state=42)
    
    # Save the train and test dataframes to CSV files
    train_filepath = os.path.join(data_dir, TRAIN_DATA_FILE)
    tes_filepath = os.path.join(data_dir, TEST_DATA_FILE)
    train_df.to_csv(train_filepath, index=False)
    test_df.to_csv(tes_filepath, index=False)


if __name__ == "__main__":
    data_df = data_preprocessing()
    data_split(data_df)
