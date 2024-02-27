import cmd
import os
from cleaner import csv_cleaner
from datetime import datetime
import pandas as pd 


# cleaner = csv_cleaner(os.path.join(os.path.dirname(__file__), "Transactions"))
# classifier = classifier(os.path.join(os.path.dirname(__file__), "Categories"))

# df = pd.concat(
#     [
#         cleaner.amex_csv(),
#         cleaner.cibc_credit_csv(),
#         cleaner.cibc_debit_csv(),
#         cleaner.tangerine_csv(),
#     ],
#     axis=0,
# )

# df = classifier.classify(df)
# df.sort_values(by="Date", ascending=False)
# print(df)

class TransactionCLI(cmd.Cmd):
    intro = 'Welcome to your Bank Transaction Classifier!\nTo begin classifying your transactions, enter a date range by typing:\n   range yyyy-mm-dd yyyy-mm-dd\n'
    prompt = '>> '

    def __init__(self, transactions, categories):
        super().__init__()
        self.transactions = transactions
        self.filtered_transactions = None
        self.start_date = None
        self.end_date = None
        self.current_transaction_index = 0
        self.categories = categories

    def do_range(self, dates):
        start_date_str, end_date_str = dates.split()
        self.start_date = pd.to_datetime(start_date_str)
        if end_date_str.lower() == "today":
            self.end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            self.end_date = pd.to_datetime(end_date_str)

        print(f"Range set for transactions between {self.start_date} and {self.end_date}")

    def do_display_transactions(self, arg):
        self.filtered_transactions = df[(df['Date'] >= self.start_date) & (df['Date'] <= self.end_date)]
        print("These are your transactions:")
        print(self.filtered_transactions)

    def do_classify_transactions(self, arg):
        for index, row in df.iterrows():
            print(f"Classify the following transaction:")
            print(row.to_markdown())
    
            for i, category in enumerate(self.categories, start=1):
                print(f"{category} [{i}]")
            category_input = input("Enter the category number or 'New [number]' for a new category: ")

            if category_input.startswith('New '):
                new_category_number = category_input.split()[1]
                new_category_name = input("Enter the name for the new category: ")
                # Implement logic to create a new category
                print(f"Created new category '{new_category_name}' with number {new_category_number}")
            else:
                print(f"Classified transaction as category {self.categories[int(category_input) - 1]}")

            self.current_transaction_index = index+1

    def do_new_category(self, arg):
        # Implement logic to create a new category
        pass

    def preloop(self):
        # Initialize your data or perform any setup before entering the loop
        pass

if __name__ == '__main__':
    cleaner = csv_cleaner(os.path.join(os.path.dirname(__file__), "Transactions"))
    df = pd.concat(
        [
            cleaner.amex_csv(),
            cleaner.cibc_credit_csv(),
            cleaner.cibc_debit_csv(),
            cleaner.tangerine_csv(),
        ],
        axis=0,
    )

    categories = ["Grocery", "Restaurant", "Shopping", "Utilities", "Entertainment", "Other"]
    df['Category'] = ''
    cli_instance = TransactionCLI(df, categories)
    cli_instance.cmdloop()
