# Copyright Michael Choi All Rights Reserved
"""driver program to parse credit card csv data"""

import argparse
import csv
import libs.cc_csv_data as cc_data

parser = argparse.ArgumentParser(description="Parse Credit Card csv file")
parser.add_argument("company",
                    help="Credit Card company",
                    choices=["brim", "mbna", "rogers", "bmo"])
parser.add_argument("filename", help="Credit Card csv file, full path")
args = parser.parse_args()

filelocation = args.filename
company = args.company

match company:
    case "brim":
        process_data = cc_data.DataBrim.initialize
        OUTPUT_FILENAME = "brim.csv"
        output_data = cc_data.DataBrim.display
        LINE_TO_SKIP = 1
    case "mbna":
        process_data = cc_data.DataMbna.initialize
        OUTPUT_FILENAME = "mbna.csv"
        output_data = cc_data.DataMbna.display
        LINE_TO_SKIP = 1
    case "rogers":
        process_data = cc_data.DataRogers.initialize
        OUTPUT_FILENAME = "rogers.csv"
        output_data = cc_data.DataRogers.display
        LINE_TO_SKIP = 1
    case "bmo":
        process_data = cc_data.DataBmo.initialize
        OUTPUT_FILENAME = "bmo.csv"
        output_data = cc_data.DataBmo.display
        LINE_TO_SKIP = 3

purchases = []
with open(filelocation, encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)

    # Skip the specified number of lines
    for _ in range(LINE_TO_SKIP):
        next(reader)

    for row in reader:
        ParsedData = process_data(row)
        if cc_data.DataCreditCard.is_purchase(ParsedData):
            purchases.append(output_data(ParsedData))

with open(OUTPUT_FILENAME, mode="w", encoding="utf-8") as output:
    for entry in purchases:
        output.write(entry)
        output.write("\n")
