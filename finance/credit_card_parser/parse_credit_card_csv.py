# Copyright Michael Choi All Rights Reserved

import argparse 
import csv 
import libs.cc_csv_data

parser = argparse.ArgumentParser(description='Parse Credit Card csv file')
parser.add_argument('company', help='Credit Card company', choices= ['brim', 'mbna', 'rogers'])
parser.add_argument('filename', help='Credit Card csv file, full path')
args = parser.parse_args()

filelocation = args.filename 
company = args.company

match company:
    case 'brim':
        process_data = libs.cc_csv_data.data_brim.initialize
        output_filename = 'brim.csv'
        output_data = libs.cc_csv_data.data_brim.display
    case 'mbna':
        process_data = libs.cc_csv_data.data_mbna.initialize
        output_filename = 'mbna.csv'
        output_data = libs.cc_csv_data.data_mbna.display
    case 'rogers':
        process_data = libs.cc_csv_data.data_rogers.initialize
        output_filename = 'rogers.csv'
        output_data = libs.cc_csv_data.data_rogers.display

purchases = []
with open(filelocation) as csvfile:
    reader = csv.reader(csvfile)    
    next(reader)
    
    for row in reader:
        parsed = process_data(row)
        if parsed.purchase:
            purchases.append(output_data(parsed))

with open(output_filename, 'w') as output:    
    for entry in purchases:
        output.write(entry)
        output.write('\n')