import timerAppAnalytics as analytics

import pandas as pd


plt = analytics.Plotter(r"timerdatabase.xlsx")


def convert_into_df(data: dict, index=[0]):

    df = pd.DataFrame(data=data, index=index)

    return df


def save_df(df):

    f = r"timerdatabase.xlsx"
    df.to_excel(f)
    

def row_data(row: int):
    data = [d for d in plt.get_data(row)]
    return data


def header_names():
    names = [col for col in plt.columns]
    return names

print(header_names())
print(row_data(0))
