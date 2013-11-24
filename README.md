## Overview

Python specs make it easy to write good python specifications for your test subjects

It has very few conventions and it provides integrations with established python testing tools like [py.test](http://pytest.org/latest/)

## Install

```
pip install specs
```

## Basic structure - [source](./examples/order_spec.py)

```python
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

## How specs are looked up and run

The test runner searches for all `*_spec.py` files that it can find in the directory (subdirectories included) where it is invoked.
From there it includes all `Context` subclasses that it can find and runs all the examples that are prefixed with `it_`.
An example is considered to be successful if it doesn't raises an Exception.
You can use any assertion library you want to form your assertions. Eg: [Sure](http://falcao.it/sure/reference.html).

## Let methods - memoized test subjects

One of the most powerful features of this library are it's `let_` methods.
Any method defined in a Context like

```python
def let_rand(self):
    return random.random()
```

can later be accessed in that context (and it's child contexts) as a property ( `self.rand` ) and it's return value will be cached
for the duration of that single example. [See example](./specs_spec.py#L30-L42)