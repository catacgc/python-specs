
class Order:

    def __init__(self, quantity, money):
        self.quantity = quantity
        self.money = money

    def currency(self):
        return self.money.currency

    def total(self):
        return self.money.value * self.quantity

class Money:

    def __init__(self, value, currency):
        self.value = value
        self.currency = currency
