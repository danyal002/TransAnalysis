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


class csv_cleaner:
    def __init__(self, basePath):
        self.basePath = basePath

    def tangerine_csv(self):
        # Tangerine marks purchases as negative values in the Amount column.
        tang_files = glob.glob(self.basePath + "/tang*.CSV")
        if not tang_files:
            return
        df = pd.concat((pd.read_csv(f, encoding="latin1") for f in tang_files))

        df.rename(columns={"Transaction date": "Date"}, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"])

        df.drop("Memo", axis=1, inplace=True)
        df.drop("Transaction", axis=1, inplace=True)

        return df

    def cibc_debit_csv(self):
        cibc_transactions = glob.glob(self.basePath + "/cibc_account.csv")
        if not cibc_transactions:
            return
        df = pd.concat((pd.read_csv(f) for f in cibc_transactions))
        df.columns = ["Date", "Name", "Debit", "Credit"]

        df["Date"] = pd.to_datetime(df["Date"])

        conditions = [(df["Credit"].notnull()), (df["Debit"].notnull())]
        values = [df["Credit"], df["Debit"] * -1]
        df["Amount"] = np.select(conditions, values)
        df.drop("Debit", axis=1, inplace=True)
        df.drop("Credit", axis=1, inplace=True)

        return df

    def cibc_credit_csv(self):
        cibc_transactions = glob.glob(self.basePath + "/cibc_aeroplan.csv")
        if not cibc_transactions:
            return
        df = pd.concat((pd.read_csv(f) for f in cibc_transactions))
        df.columns = ["Date", "Name", "Debit", "Credit", "Card"]

        df.drop("Card", axis=1, inplace=True)

        conditions = [(df["Credit"].notnull()), (df["Debit"].notnull())]
        values = [df["Credit"], df["Debit"] * -1]
        df["Amount"] = np.select(conditions, values)
        df.drop("Debit", axis=1, inplace=True)
        df.drop("Credit", axis=1, inplace=True)

        df["Date"] = pd.to_datetime(df["Date"])

        return df

    def amex_csv(self):
        amex_transactions = glob.glob(self.basePath + "/amex.csv")
        if not amex_transactions:
            return
        df = pd.concat((pd.read_csv(f) for f in amex_transactions))

        df.columns = ["Date", "Ref", "Amount", "Name", "drop1", "drop2"]
        df.drop("Ref", axis=1, inplace=True)
        df.drop("drop1", axis=1, inplace=True)
        df.drop("drop2", axis=1, inplace=True)

        df["Date"] = pd.to_datetime(df["Date"])

        df["Amount"] = df["Amount"].apply(lambda x: x * -1)

        return df




# Right now, I have to put in the categories manually. however, what if it did some of the work
# for me and asked me about the categories it didn't recognize from the transaction?
# In such a case, I can interact with the program on the terminal and have a flag for this. If
# the flag for manual classification is true, it will ask me. Otherwise, its NAN.
# So, I want it to remember the things i've classified already. I also want an easier way
# to classify. One way to do this is tokenization and cleanup.
# Once the correct transaction "company" name is chosen, the program should look for a
# similar company name in the lists and if found, it should place the new name in that category.
# otherwise, it should ask me for the category to classify it as.

# In order to do this, the program should output the choices and stop until input is specified.
