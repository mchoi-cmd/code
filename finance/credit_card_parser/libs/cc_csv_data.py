# Copyright Michael Choi All Rights Reserved
"""module containing class for credit card csv data"""

class DataCreditCard:
    """class representing generic credit card data"""

    def __init__(self, posted_date, description, amount):
        self.posted_date = posted_date
        self.description = description
        self.amount = amount.replace(',', '')
        self.purchase = False

    def display(self):
        """display posted date, description and amount"""
        output_string = self.posted_date + "," + self.description + "," + self.amount
        return output_string

    def is_purchase(self):
        """check if the transaction is a purchase"""
        return self.purchase


class DataBrim(DataCreditCard):
    """class representing BRIM credit card data"""
    # BRIM columns
    # 0 ['No',
    # 1 'Transaction Date',
    # 2 'Posted Date',
    # 3 'Description',
    # 4 'Amount',
    # 6 'Points',
    # 7 'Category']
    payment_filter = ["Redemption", "Refund", "Payment"]

    def __init__(self, line):
        DataCreditCard.__init__(self, line[2], line[3], line[4])
        self.transaction_date = line[1]
        self.category = line[6]
        self.purchase = self.category not in self.payment_filter
        # if self.category not in self.payment_filter:
        #     self.purchase = True

    @classmethod
    def initialize(cls, line):
        """public method to initialize the class"""
        cls.__init__(cls, line)
        return cls


class DataMbna(DataCreditCard):
    """class representing MBNA credit card data"""
    # MBNA columns
    # 0 Posted Date,
    # 1 Payee,
    # 2 Address,
    # 3 Amount
    payment_filter = ["CASH REWARD", "PAYMENT"]

    def __init__(self, line):
        DataCreditCard.__init__(self, line[0], line[1], line[3])
        self.purchase = self.description not in self.payment_filter

    def __str__(self):
        return self.posted_date + "," + self.description + "," + self.amount.replace('-', '')

    @classmethod
    def initialize(cls, line):
        """public method to initialize the class"""
        cls.__init__(cls, line)
        return cls


class DataRogers(DataCreditCard):
    """class representing Rogers credit card data"""
    # ROGERS column
    # 0 "Date",
    # 1 "Posted Date",
    # 2 "Reference Number",
    # 3 "Activity Type",
    # 4 "Status",
    # 5 "Transaction Card Number",
    # 6 "Merchant Category",
    # 7 "Merchant Name",
    # 8 "Merchant City",
    # 9 "Merchant State/Province",
    # 10 "Merchant Country",
    # 11 "Merchant Postal Code/Zip",
    # 12 "Amount",
    # 13 "Rewards",
    # 14 "Name on Card"
    payment_filter = ["CashBack / Remises", "PAYMENT, THANK YOU"]

    def __init__(self, line):
        DataCreditCard.__init__(self, line[1], line[7], line[12])
        self.transaction_date = line[0]
        if self.description not in self.payment_filter and self.amount[0] != "-":
            self.purchase = True

    @classmethod
    def initialize(cls, line):
        """public method to initialize the class"""
        cls.__init__(cls, line)
        return cls

class DataBmo(DataCreditCard):
    """class representing BMO credit card data"""
    # bmo column
    # 0 Item #
    # 1 Card #
    # 2 Transaction Date
    # 3 Posting Date
    # 4 Transaction Amount
    # 5 Description
    payment_filter = ["CashBack / Remises", "PAYMENT, THANK YOU"]

    def __init__(self, line):
        DataCreditCard.__init__(self, line[3], line[5], line[4])
        self.transaction_date = line[2]
        self.purchase = (self.description not in self.payment_filter and self.amount[0] != "-")

    @classmethod
    def initialize(cls, line):
        """public method to initialize the class"""
        cls.__init__(cls, line)
        return cls
