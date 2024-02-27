import numpy as np  # to cleanse data
import os

class classifier:
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

    def manual_classify(self, df):
        return df

    def classify(self, df):
        if df.empty:
            return
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

        df["Category"] = np.where(
            df["Category"].str.contains("nan", case=False, regex=False),
            self.manual_classify(
                df["Category"]
            ),  # How to run a function on every row in a pandas df?
            df["Category"],
        )

        return df