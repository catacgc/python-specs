from pspec import Context, run_all

class DescribeLet(Context):
    A = 1

    def let_a(self): return self.A
    def let_b(self): return 2
    def let_sum(self): return self.b + self.a

    def it_should_evaluate_let_blocks_as_attributes(self):
        assert self.sum == 3

    def it_should_prefer_overwritten_attributes(self):
        self.A = 2
        assert self.sum == 4

    def it_should_not_produce_side_effects(self):
        assert self.A == 1

    class SubContext(Context):

        def let_a(self): return 2

        def it_should_use_variables_from_parent_context(self):
            assert self.sum == 4

        def it_can_access_state_from_parent_context(self):
            assert self.A == 1

class DescribeLetMemoizesValues(Context):
    COUNTER = 0

    def let_a(self):
        self.__class__.COUNTER += 1
        return self.COUNTER

    def it_memoizes_the_value(self):
        assert self.a == 1
        assert self.a == 1

    def it_is_not_cached_across_examples(self):
        assert self.a == 2

class DescribeBeforeHooks(Context):

    def let_test(self): return 1

    def before(self):
        self.test += 1

    def it_should_run_before_the_example(self):
        assert self.test == 2

    class SubContext(Context):

        def before(self):
            self.test += 1

        def it_should_run_both_before_blocks(self):
            assert self.test == 3

class DescribeAfterHooks(Context):
    RUN_ORDER = []

    def after(self):
        assert DescribeAfterHooks.RUN_ORDER == [1, 2]

    class SubContext(Context):

        def after(self):
            DescribeAfterHooks.RUN_ORDER.append(2)

        def it_should_run_after_examples(self):
            DescribeAfterHooks.RUN_ORDER.append(1)

class DescribeContextNesting(Context):
    def let_a(self): return self.one
    def let_one(self): return 1

    class First(Context):
        def let_a(self): return self.parent.a + 1

        class Second(Context):
            def let_a(self): return self.parent.a + 1

            def it_should_be_3(self):
                assert self.a == 3

if __name__ == '__main__':
    run_all([
        DescribeLet,
        DescribeLetMemoizesValues,
        DescribeBeforeHooks,
        DescribeAfterHooks,
        DescribeContextNesting,
    ])