## Documentation

Detailed documentation can be found at http://pspecs.readthedocs.org/en/latest/

## Overview

*pspecs* is a testing library that concentrates on making it easy to build test subjects, isolate test runs
and write readable specifications

It has very few conventions and it provides integrations with established
python testing tools like [py.test](http://pytest.org/latest/) or [nose](http://nose.readthedocs.org/en/latest/)

## Install

```
pip install pspecs
```

## Basic structure - [source](./examples/order_spec.py)

```python
from pspecs import Context

class OrderSpec(Context):

    def let_quantity(self): return 10
    def let_money(self):
        return Money(10, 'USD')

    def let_order(self):
        return Order(self.quantity, self.money)

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
                return Money(10, 'EUR')

            def it_should_be_euros(self):
                assert self.currency == 'EUR'
```

## Running the specs

With nose: 'nosetests --with-specs'