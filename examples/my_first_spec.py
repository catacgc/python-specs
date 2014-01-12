# my_first_spec.py
from pspecs import Context, let

class DescribeMath(Context):

    @let
    def numbers(self):
        return [1, 2, 3]

    class DescribeSum(Context):

        @let
        def sum(self):
            return sum(self.numbers)

        def it_should_be_six(self):
            assert self.sum == 6

    class DescribeProd(Context):

        @let
        def prod(self):
            return reduce(lambda a, b: a*b, self.numbers, 1)

        def it_should_be_six(self):
            assert self.prod == 6