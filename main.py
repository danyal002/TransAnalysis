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

        df.drop("Memo", axis=1, inplace=True)
        df.drop("Transaction", axis=1, inplace=True)

        return df

    def cibc_debit_csv(self):
        cibc_transactions = glob.glob(self.basePath + "/cibc_account.csv")
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
        df = pd.concat((pd.read_csv(f) for f in amex_transactions))

        df.columns = ["Date", "Ref", "Amount", "Name", "drop1", "drop2"]
        df.drop("Ref", axis=1, inplace=True)
        df.drop("drop1", axis=1, inplace=True)
        df.drop("drop2", axis=1, inplace=True)

        df["Date"] = pd.to_datetime(df["Date"])

        df["Amount"] = df["Amount"].apply(lambda x: x * -1)

        return df


class classifcation:
    def __init__(self, basePath):
        self.basePath = basePath
        self.categories = self.get_categories()

    def get_categories(self):
        categories = {}
        category_directory = os.fsdecode(self.basePath)
        for file in os.listdir(category_directory):
            filename = os.fsdecode(file)
            with open(category_directory + "/" + file, "r") as infile:
                for line in infile:
                    categories[line.strip()] = filename.replace(".txt", "").title()
        return categories

    def classify(self, df):
        df["Category"] = np.nan
        for key, value in self.categories.items():
            df["Category"] = np.where(
                df["Name"].str.contains(key, case=False, regex=False),
                value,
                df["Category"],
            )

        e_transfer_in_cond = (
            df["Name"].str.contains("e-transfer", case=False, regex=False)
        ) & (df["Amount"] > 0)
        df.loc[e_transfer_in_cond, "Category"] = "Transfer In"

        e_transfer_out_cond = (
            df["Name"].str.contains("e-transfer", case=False, regex=False)
        ) & (df["Amount"] < 0)
        df.loc[e_transfer_out_cond, "Category"] = "Transfer Out"

        electronic_funds_in_cond = (
            (
                df["Name"].str.contains(
                    "electronic funds transfer", case=False, regex=False
                )
            )
            & (df["Amount"] > 0)
            & ~(df["Name"].str.contains("pay", case=False, regex=False))
        )
        df.loc[electronic_funds_in_cond, "Category"] = "Transfer In"

        electronic_funds_out_cond = (
            df["Name"].str.contains(
                "electronic funds transfer", case=False, regex=False
            )
        ) & (df["Amount"] < 0)
        df.loc[electronic_funds_out_cond, "Category"] = "Transfer Out"

        return df


cleaner = csv_cleanup(os.path.join(os.path.dirname(__file__), "Transactions"))
classifier = classifcation(os.path.join(os.path.dirname(__file__), "Categories"))

df = pd.concat(
    [
        cleaner.amex_csv(),
        cleaner.cibc_credit_csv(),
        cleaner.cibc_debit_csv(),
        cleaner.tangerine_csv(),
    ],
    axis=0,
)

df = classifier.classify(df)
df.sort_values(by="Date", ascending=False)
