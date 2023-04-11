# Copyright Michael Choi All Rights Reserved

import argparse 
import csv 

class data_rogers:    
    # ROGERS column 
    # "Date","Posted Date","Reference Number","Activity Type","Status","Transaction Card Number","Merchant Category","Merchant Name","Merchant City","Merchant State/Province","Merchant Country","Merchant Postal Code/Zip","Amount","Rewards","Name on Card"
    payment_filter = ["CashBack / Remises", "PAYMENT, THANK YOU"]

    def __init__(self, transaction_date, posted_date, description, amount):
        self.transaction_date = transaction_date
        self.posted_date = posted_date
        self.description = description
        self.amount = amount
    def __str__(self):
        return self.transaction_date + "," + self.posted_date + "," +  self.description + "," +  self.amount

parser = argparse.ArgumentParser(description='Parse Rogers csv file')
parser.add_argument('filename', help='Rogers csv file, full path')
args = parser.parse_args()

filelocation = args.filename 

purchases = []
with open(filelocation) as csvfile:
    reader = csv.reader(csvfile)    
    next(reader)
    
    for row in reader:
        parsed = data_rogers(row[0], row[1], row[7], row[12])
        if parsed.description not in parsed.payment_filter and parsed.amount[0] != "-":
            purchases.append(parsed)

with open("rogers.csv", 'w') as output:    
    for entry in purchases:
        output.write(str(entry))
        output.write('\n')
