
import pandas as pd



class Plotter():

    def __init__(self, datafile):
        self.df = pd.read_excel(datafile, index_col=0)
        self.columns = self.df.columns

    def get_data(self, row):
        return self.df.iloc[row]


if __name__ == "__main__":
    plt = Plotter(r"timerdatabase.xlsx")
#    print(plt.df)
#    print(plt.df.iloc[0])
    cols = [col for col in plt.columns]
    print(cols)
