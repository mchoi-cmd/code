# Copyright Michael Choi All Rights Reserved

import argparse
import csv

class data_mbna:
    # MBNA column
    # Posted Date,Payee,Address,Amount
    payment_filter = ["CASH REWARD", "PAYMENT"]

    def __init__(self, posted_date, description, amount):
        self.posted_date = posted_date
        self.description = description
        self.amount = amount
    def __str__(self):
        return self.posted_date + "," +  self.description + "," +  self.amount.replace('-', '')

parser = argparse.ArgumentParser(description='Parse MBNA csv file')
parser.add_argument('filename', help='MBNA csv file, full path')
args = parser.parse_args()

filelocation = args.filename

purchases = []
with open(filelocation) as csvfile:
    reader = csv.reader(csvfile)
    next(reader)

    for row in reader:
        parsed = data_mbna(row[0], row[1], row[3])
        if parsed.description not in parsed.payment_filter:
            purchases.append(parsed)

with open("mbna.csv", 'w') as output:
    for entry in purchases:
        output.write(str(entry))
        output.write('\n')
