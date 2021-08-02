
import pandas as pd


def convert_into_df(data: dict, index=[0]):

    df = pd.DataFrame(data=data, index=index)

    return df


def save_df(df):

    f = r"timerdatabase.xlsx"
    df.to_excel(f)


def read_df(f):

    df = pd.read_excel(f)

    return df



