# Copyright Michael Choi All Rights Reserved


class data_credit_card:
    def __init__(self, posted_date, description, amount):
        self.posted_date = posted_date
        self.description = description
        self.amount = amount
        self.purchase = False


class data_brim(data_credit_card):
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
        data_credit_card.__init__(self, line[2], line[3], line[4])
        self.transaction_date = line[1]
        self.category = line[6]
        if self.category not in self.payment_filter:
            self.purchase = True

    def __str__(self):
        return self.posted_date + "," + self.description + "," + self.amount

    @classmethod
    def initialize(self, line):
        self.__init__(self, line)
        return self

    def display(self):
        output_string = self.__str__(self)
        return output_string

class data_mbna(data_credit_card):
    # MBNA columns
    # 0 Posted Date,
    # 1 Payee,
    # 2 Address,
    # 3 Amount
    payment_filter = ["CASH REWARD", "PAYMENT"]

    def __init__(self, line):
        data_credit_card.__init__(self, line[0], line[1], line[3])
        if self.description not in self.payment_filter:
            self.purchase = True

    def __str__(self):
        return self.posted_date + "," + self.description + "," + self.amount.replace('-', '')

    @classmethod
    def initialize(self, line):
        self.__init__(self, line)
        return self

    def display(self):
        output_string = self.__str__(self)
        return output_string

class data_rogers(data_credit_card):
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
        data_credit_card.__init__(self, line[1], line[7], line[12])
        self.transaction_date = line[0]
        if self.description not in self.payment_filter and self.amount[0] != "-":
            self.purchase = True

    def __str__(self):
        return self.posted_date + "," + self.description + "," + self.amount

    @classmethod
    def initialize(self, line):
        self.__init__(self, line)
        return self

    def display(self):
        output_string = self.__str__(self)
        return output_string
