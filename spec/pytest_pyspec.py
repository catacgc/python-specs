import pytest


def pytest_addoption(parser):
    """Add option to collect Konira test cases"""
    group = parser.getgroup('pyspec group')
    group.addoption('--spec', action='store_true', help='Collects PySpec test cases')



def pytest_collect_file(path, parent):
    if parent.config.option.spec and path.basename.lower().startswith("case_"):
        return SpecFile(path, parent)



class SpecFile(pytest.File):
    def collect(self):
        classes = get_classes(self.fspath.strpath, None)

        for case in classes:

            # Initialize the test class
            suite = case()

            # check test environment setup
            environ = TestEnviron(suite)

            methods = get_methods(suite, None)
            if not methods: return

            # Are we skipping?
            if safe_skip_call(environ.set_skip_if):
                return

            let_attrs = get_let_attrs(suite)

            # Set before all if any
            environ.set_before_all()

            for test in methods:
                yield KoniraItem(str(test), self, suite, test, let_attrs)

            # Set after all if any
            environ.set_after_all()



class SpecItem(pytest.Item):


    def __init__(self, name, parent, case, spec, let_attrs):
        super(KoniraItem, self).__init__(name, parent)
        self.spec = spec
        self.let_attrs = let_attrs
        self.case = set_let_attrs(case, let_attrs)


    def runtest(self):
        # check test environment setup
        environ = TestEnviron(self.case)

        # Set before each if any
        environ.set_before_each()

        case = set_let_attrs(self.case, self.let_attrs)
        getattr(case, self.spec)()

        # Set after each if any
        environ.set_after_each()

    def reportinfo(self):
        describe = "describe %s" % name_convertion(self.case.__class__.__name__)
        it = name_convertion(self.name, capitalize=False)
        describe_and_it = "%s ==>> %s" % (describe, it)
        return self.fspath, 0, describe_and_it