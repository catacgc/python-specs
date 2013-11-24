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

## Concepts

### Context

A class that describes the behaviour for a test subject and it's comprised of Let Methods,
Examples, Hooks or other Spec Contexts. It always subclasses the `Context` class

```python
class OrderSpec(Context):
    pass
```

### Example

A method in a Spec Context that begins with `it_` and represents an atomic test unit.
Usually an example asserts something about a test subject

```python
def it_should_do_something(self):
    assert self.subject == 'do something'
```

### Let Methods

One of the most powerful features of this library are it's `let_` methods.
Any method defined in a Context like

```python
def let_rand(self):
    return random.random()
```

can later be accessed in that context (and it's child contexts) as a property ( `self.rand` ) and it's return value will be cached
for the duration of a single example. [See example spec](./specs_spec.py#L30-L42)

These methods are evaluated when an example accesses a property with the name following the `let_` prefix.
Eg: the method with the name `let_something` will be evaluated only when it will be accessed in an
 example: `self.something`. The return value of the method will be cached for the duration of that
 single example

```python
def let_a(self): return 1
def let_b(self): return 2
def let_sum(self): return self.a + self.b

def it_should_sum_up(self):
    assert self.sum == 3
```

### Before And Hooks

 There are two types of hooks: `before` and `after`. These are methods defined in a context and, as the name implies,
 they are run automatically before each example from that context.
 The parent hooks will also run for child context examples in the expected order

```python
class Parent(Context):
    def before(self): print 'Runs first'

    class Child(Context):
        def before(self): print 'Runs second'

        def it_should_run(self):
            print 'Runs third'

```