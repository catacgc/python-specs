from pspecs import Context, let
from nose.tools import raises

class BaseFunctionality(Context):

    def __init__(self):
        """ The init method is available unaltered to a context
         There's no need to call super
        """

        self.execution = []

    @let
    def a(self):
        """ @let is similar in function with @property with one difference that
        it memoizes the returned value for subsequent calls
        """

        return 1

    def before(self):
        """ Called before each test case """

        self.do('before parent')

    def after(self):
        self.do('after parent')

    def it_should_be_equal(self):
        """ This is the actual test case that will run.
        By convention all test cases must start with it_ or test_.
        Usually this is the place where you run assertions on your test subjects
        """

        assert self.a == 1
        self.do('it_should_be_equal')

    def do(self, what):
        self.execution.append(what)

    class ChildContext(Context):
        """ A child context has access to all properties of it's parent context. Think of it
        as subclassing, but only for attribute access (methods are not inherited by the child context)
        """

        def before(self):
            """ A child context can have before / after hooks.
            As expected they will be run along with the hooks from the parent context
            """
            self.do('before child')

        def after(self):
            self.do('after child')

        @let
        def b(self):
            """ Another example of test subject set-up.
            It's using the value of the 'self.a' test subject from the parent
            """
            return self.a + 1

        def test_also_works(self):
            assert self.b == 2
            self.do('test_also_works')

class TestExceptions(Context):

    @raises(AttributeError)
    def it_should_raise_error_for_missing_attributes(self):
        self.missing_attribute

class DescribeBaseFunctionality(Context):

    @let
    def parent_context(self):
        return BaseFunctionality

    @let
    def child_context(self):
        return self.parent_context.children_contexts()[0]

    class ParentContext(Context):

        def it_should_discover_two_examples(self):
            examples = self.parent_context.discovered_test_cases()
            assert 2 == len(examples)

    class ChildContext(Context):

        def it_should_discover_before_hooks_from_parent(self):
            hooks = self.child_context.hooks('before')
            assert len(hooks) == 2

            hooks = self.child_context.hooks('after')
            assert len(hooks) == 2

    class DiscoveryOfTestCases(Context):

        @let
        def test_cases(self):
            return self.parent_context.discovered_test_cases()

        @let
        def parent_test(self):
            return self.test_cases[0]

        @let
        def child_test(self):
            return self.test_cases[1]

        def it_should_discover_one_test_example(self):
            assert len(self.test_cases) == 2
            assert self.child_test.name().find('test_also_works') != -1

        def it_should_run_hooks(self):
            self.parent_test.run()
            execution = self.parent_test.context.execution
            assert execution == ['before parent', 'it_should_be_equal', 'after parent']

        def it_should_run_all_hooks_from_parent(self):
            self.child_test.run()
            execution = self.child_test.context.parent.execution
            assert execution == ['before parent', 'before child', 'test_also_works', 'after child', 'after parent']