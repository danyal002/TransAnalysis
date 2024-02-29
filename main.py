import cmd
import os
from cleaner import csv_cleaner
from datetime import datetime
import pandas as pd 

class TransactionCLI(cmd.Cmd):
    intro = 'Welcome to your Bank Transaction Classifier!\nTo begin classifying your transactions, enter a date range by typing:\n   range yyyy-mm-dd yyyy-mm-dd\n'
    prompt = '>> '

    def __init__(self, transactions, categories):
        super().__init__()
        self.transactions = transactions
        self.start_date = pd.to_datetime("2020-01-01")
        self.end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
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

    def do_display(self, arg):
        print(f"Displaying transactions from {self.start_date} to {self.end_date}:")
        print(self.transactions[(self.transactions['Date'] >= self.start_date) & (self.transactions['Date'] <= self.end_date)])

    def do_classify(self, arg):
        transactions = self.transactions[(self.transactions['Date'] >= self.start_date) & (self.transactions['Date'] <= self.end_date)]
        for index, row in transactions.iterrows():
            print(f"Classify transaction {self.current_transaction_index + 1} of {len(self.transactions)}:")
            print(row.to_markdown(tablefmt="simple_grid"))
    
            for i, val in enumerate(self.categories, start=1):
                print(f"{val}[{i}]", end=' ')
            print(f"New[{len(self.categories) + 1}] Skip[{len(self.categories) + 2}]")
            
            category_input = input("Enter category number: ")

            if category_input == "exit":
                break

            if category_input.startswith(f'{len(self.categories) + 1}'):
                new_category_number = category_input.split()[0]
                new_category_name = input("Enter the name for the new category: ").title()
                self.categories.append(new_category_name)
                print(f"Created new category '{new_category_name}' with number {new_category_number}")
            elif category_input.startswith(f'{len(self.categories) + 2}'):
                print("Skipping transaction...")
                self.current_transaction_index = index + 1
                continue
            
            self.transactions.at[self.current_transaction_index, 'Category'] = self.categories[int(category_input) - 1]
            print(f"Classified transaction as {self.categories[int(category_input) - 1]}")

            self.current_transaction_index = index + 1

    def do_expense(self, arg):
        self.transactions['Absolute_Amounts'] = self.transactions['Amount'].abs()
        category_sums = self.transactions.groupby('Category')['Absolute_Amounts'].sum()
        print(category_sums)

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
        ignore_index=True
    )
    df.sort_values(by="Date", ascending=True)
    
    categories = ["Grocery", "Restaurant", "Shopping", "Utilities", "Entertainment", "Other"]
    df['Category'] = ''
    cli_instance = TransactionCLI(df, categories)
    cli_instance.cmdloop()
