# Copyright Michael Choi All Rights Reserved

import argparse
import csv


class data_brim:
    # BRIM column
    # ['No', 'Transaction Date', 'Posted Date', 'Description', 'Cardmember', 'Amount', 'Points', 'Category']
    payment_filter = ["Redemption", "Refund", "Payment"]

    def __init__(self, transaction_date, posted_date, description, amount, category):
        self.transaction_date = transaction_date
        self.posted_date = posted_date
        self.description = description
        self.amount = amount
        self.category = category

    def __str__(self):
        return self.transaction_date + "," + self.posted_date + "," +  self.description + "," +  self.amount

parser = argparse.ArgumentParser(description='Parse BRIM csv file')
parser.add_argument('filename', help='BRIM csv file, full path')
args = parser.parse_args()

filelocation = args.filename

purchases = []
with open(filelocation) as csvfile:
    reader = csv.reader(csvfile)
    next(reader)

    for row in reader:
        parsed = data_brim(row[1], row[2], row[3], row[5], row[7])
        if parsed.category not in parsed.payment_filter:
            purchases.append(parsed)


with open("brim.csv", 'w') as output:
    for entry in purchases:
        output.write(str(entry))
        output.write('\n')
