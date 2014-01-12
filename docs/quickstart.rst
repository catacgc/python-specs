Quickstart
==========

Installation
------------

>>> pip install pspecs

Basic structure
---------------

.. literalinclude:: ../examples/my_first_spec.py
    :lines: 1-


It should be fairly easily to spot what's being tested here: the sum and the product of a sequence of integers.

You will notice few off the simple and powerful concepts in `pspecs`:
:doc:`Memoized let methods<let_methods>` and :doc:`Parent and children contexts<contexts>`.


Running
-------

`pspecs` doesn't provide it's own runner yet. Instead, it relies on well known test runners like py.test_ or nose_

Running with nose:

>>> nosetests --with-specs my_first_spec.py

.. _py.test: http://pytest.org/latest/
.. _nose: http://nose.readthedocs.org/en/latest/



Tests narratives
----------------

Given a spec file **order_spec.py**

.. literalinclude:: ../examples/order_spec.py
    :lines: 2-
    :linenos:

The purpose of any testing library is to make it easy for anybody looking at it to spot quickly what's being tested.

Looking at the code above and reading only the class names and the `it_` method names, we can discover a narrative::

    DescribeOrder
        DescribeOrderTotal
            it_should_account_for_quantity
            WithEmptyContext
                it_should_be_zero
        DescribeOrderCurrency
            it_should_be_dollars
            WithEuros
                it_should_be_euros


What `pspec` does is exactly to allow such kind of narratives to be built easily using simple, yet powerful concepts like
`contexts`, `memoized let methods`, `hooks` and `isolated tests`




