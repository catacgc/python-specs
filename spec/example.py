import inspect

def run(context, parent_context=None, let={}):
    examples, sub_contexts = {}, {}
    for name, the_type in context.__dict__.items():
        if name.find('it_') == 0:
            examples[name] = the_type

        if name.find('let_') == 0:
            let[name[4:]] = the_type

        if inspect.isclass(the_type):
            sub_contexts[name] = the_type

    for name, example in examples.items():
        context(parent_context, let).run(example)

    for name, sub_context in sub_contexts.items():
        new_parent_context = context(parent_context, let)
        run(sub_context, new_parent_context, let)


class Context(object):

    def __init__(self, parent_context=None, let={}):
        self._parent_context = parent_context
        self._let = let

    def before(self):
        pass

    def after(self):
        pass

    def __getattr__(self, attr):
        if attr in self._let:
            return self._attr(attr)

        if self._parent_context:
            return getattr(self._parent_context, attr)

        raise AttributeError("Attribute %s not found" % attr)

    def _attr(self, attr):
        value = self._let[attr](self)
        setattr(self, attr, value)
        
        return getattr(self, attr)

    def _before(self):
        self._parent_context and self._parent_context._before()
        self.before()

    def _after(self):
        self._parent_context and self._parent_context._after()
        self.after()

    def run(self, example_method):
        self._before()
        example_method(self)
        self._after()


class DescribeLet(Context):

    def let_a(self): return 1
    def let_b(self): return 2
    def let_sum(self):
        return self.b + self.a

    def it_should_evaluate_let_blocks_as_attributes(self):
        assert self.sum == 3

    def it_should_prefer_overwritten_attributes(self):
        self.a = 2
        assert self.sum == 4

    def it_should_not_produce_side_effects(self):
        assert self.sum == 3

    class SubContext(Context):

        def let_a(self): return 2

        def it_should_use_variables_from_outer_scope(self):
            assert self.sum == 4

class DescribeLetMemoizeValues(Context):
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

    def let_dict(self): return {}

    def before(self):
        self.dict['a'] = 1

    def it_should_run_before_the_example(self):
        assert self.dict['a'] == 1

    class SubContext(Context):

        def before(self):
            print self.dict
            self.dict['a'] += 1

        def it_should_run_both_before_blocks(self):
            assert self.dict['a'] == 2

run(DescribeLet)
run(DescribeLetMemoizeValues)
run(DescribeBeforeHooks)