import pandas as pd
from sklearn.model_selection import train_test_split
import typing

from aws_logger import logger


def data_preprocessing(matches_df: pd.DataFrame) -> typing.Tuple[pd.DataFrame, pd.Series]:

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

    features = ['Series', 'Court', 'Surface', 'Player_1', 'Player_2', 'Rank_1', 'Rank_2', 'Pts_1', 'Pts_2', 'Odd_1', 'Odd_2']
    x = matches_df[features]
    y = matches_df['Label']

    return x, y


def data_split(x: pd.DataFrame, y: pd.Series) -> typing.Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    return x_train, x_test, y_train, y_test