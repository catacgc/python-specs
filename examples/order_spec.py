from .order import *
from pspecs import Context

class DescribeOrder(Context):

    def let_quantity(self): return 10
    def let_money(self):
        return Money(10, self.type)

    def let_type(self):
        return 'USD'

    def let_order(self):
        return Order(self.quantity, self.money)

    class DescribeOrderTotal(Context):
        def let_total(self):
            return self.order.total()

        def it_should_account_for_quantity(self):
            assert self.total == 100

        class WithEmptyQuantity(Context):
            def let_quantity(self): return 0

            def it_should_be_zero(self):
                assert self.total == 0

    class DescribeOrderCurrency(Context):
        def let_currency(self):
            return self.order.currency()

        def it_should_be_dollars(self):
            assert self.currency == 'USD'

        class WithEuros(Context):

            def it_should_be_euros(self):
                self.type = 'EUR'
                assert self.currency == 'EUR'