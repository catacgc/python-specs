## Overview

Python specs make it easy to write good python specifications for your test subjects

It has very few conventions and it provides integrations with established python testing tools like [py.test](http://pytest.org/latest/)

## Install

```
pip install specs
```

## Basic structure

```
# ./order_spec.py
class OrderSpec(Context):

 def let_quantity(self): return 10
 def let_money(self):
    return Money(10, 'USD')

 def let_order(self):
    return new Order(self.quantity, self.money)

 class OrderTotal(Context):
     def let_total(self):
        return self.order.total()

     def it_should_account_for_quantity(self):
        assert self.total == 100

     class WithEmptyQuantity(Context):
        def let_quantity(self): return 0

        def it_should_be_zero(self):
            assert self.total == 0

 class OrderCurrency(Context):
    def let_currency(self):
        return self.order.currency()

    def it_should_be_dollars(self):
        assert self.currency == 'USD'

    class WithEuros(Context):
        def let_money(self):
            return new Money(10, 'EUR')

        def it_should_be_euros(self):
            assert.self.currency == 'EUR'
```

## Running the specs

With py.test: `py.test --specs`

With specs.py: `specs.py`

```
order spec:
    order total:
        it should account for quantity
        with empty quantity:
            it should be zero
    order currency:
        it should be dollars
        with euros:
            it should be euros
```