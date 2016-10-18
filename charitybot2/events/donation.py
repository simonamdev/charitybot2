class InvalidArgumentException(Exception):
    pass


class Donation:
    currency_symbols = ['$', '£', '€']

    def __init__(self, old_amount, new_amount):
        self.old_amount = self.parse_donation_input(old_amount)
        self.new_amount = self.parse_donation_input(new_amount)
        self.validate_resultant_amounts()
        self.donation_amount = self.new_amount - self.old_amount

    def parse_donation_input(self, amount):
        if amount == '':
            raise InvalidArgumentException
        if isinstance(amount, str):
            amount = amount.replace(',', '')
            for symbol in self.currency_symbols:
                amount = amount.replace(symbol, '')
        return int(float(amount))

    def validate_resultant_amounts(self):
        if self.new_amount < self.old_amount:
            raise InvalidArgumentException

    def get_donation_amount(self):
        return self.donation_amount
