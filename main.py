import pandas as pd  # to perform data manipulation and analysis
import numpy as np  # to cleanse data
import glob
import os
from datetime import datetime  # to manipulate dates
import plotly.express as px  # to create interactive charts
import plotly.graph_objects as go  # to create interactive charts

# from jupyter_dash import JupyterDash  # to build Dash apps from Jupyter environments
# from dash import dcc  # to get components for interactive user interfaces
# from dash import html  # to compose the dash layout using Python structures\


class csv_cleanup:
    def __init__(self, basePath):
        self.basePath = basePath

    def tangerine_csv(self):
        # Tangerine marks purchases as negative values in the Amount column.
        tang_files = glob.glob(self.basePath + "/tang*.CSV")
        df = pd.concat((pd.read_csv(f, encoding="latin1") for f in tang_files))

        df.rename(columns={"Transaction date": "Date"}, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values(by="Date", ascending=False)

        df.drop("Memo", axis=1, inplace=True)
        df.drop("Transaction", axis=1, inplace=True)

        return df

    def cibc_debit_csv(self):
        cibc_transactions = glob.glob(self.basePath + "/cibc_account.csv")
        df = pd.concat((pd.read_csv(f) for f in cibc_transactions))
        df.columns = ["Date", "Name", "Debit", "Credit"]

        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values(by="Date", ascending=False)

        conditions = [(df["Credit"].notnull()), (df["Debit"].notnull())]
        values = [df["Credit"], df["Debit"] * -1]
        df["Amount"] = np.select(conditions, values)
        df.drop("Debit", axis=1, inplace=True)
        df.drop("Credit", axis=1, inplace=True)

        return df

    def cibc_credit_csv(self):
        cibc_transactions = glob.glob(self.basePath + "/cibc_aeroplan.csv")
        df = pd.concat((pd.read_csv(f) for f in cibc_transactions))
        df.columns = ["Date", "Name", "Debit", "Credit", "Card"]

        df.drop("Card", axis=1, inplace=True)

        conditions = [(df["Credit"].notnull()), (df["Debit"].notnull())]
        values = [df["Credit"], df["Debit"] * -1]
        df["Amount"] = np.select(conditions, values)
        df.drop("Debit", axis=1, inplace=True)
        df.drop("Credit", axis=1, inplace=True)

        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values(by="Date", ascending=False)

        return df

    def amex_csv(self):
        amex_transactions = glob.glob(self.basePath + "/amex.csv")
        df = pd.concat((pd.read_csv(f) for f in amex_transactions))

        df.columns = ["Date", "Ref", "Amount", "Name", "drop1", "drop2"]
        df.drop("Ref", axis=1, inplace=True)
        df.drop("drop1", axis=1, inplace=True)
        df.drop("drop2", axis=1, inplace=True)

        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values(by="Date", ascending=False)

        df["Amount"] = df["Amount"].apply(lambda x: x * -1)

        return df


class classifcation:
    """
    There's going to be a list of categories. Each category will have it's own text file.
    We can have a hashmap of EntityName:Category.
    We can create this hashmap by reading from the individual files.
    All you would have to do is create a new file in the Categories folder and that category will be added.
    """

    def __init__(self, basePath):
        self.basePath = basePath
        self.categories = {}

    # loop over the base path
    # read in each file
    # take the contents of that file and map them into the hashmap with value:file_name

    def get_categories(self):
        category_directory = os.fsdecode(self.basePath)
        for file in os.listdir(category_directory):
            filename = os.fsdecode(file)
            self.categories.append()


obj = csv_cleanup(os.path.join(os.path.dirname(__file__), "Transactions"))
obj2 = classifcation(os.path.join(os.path.dirname(__file__), "Categories"))
obj2.get_categories()
# print(obj.amex_csv())
# print(obj.cibc_credit_csv())
# print(obj.cibc_debit_csv())
# print(obj.tangerine_csv())
