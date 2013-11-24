import pytest
from specs import Context, Runner
import inspect
import imp
import os

def pytest_addoption(parser):
    group = parser.getgroup('specs group')
    group.addoption('--specs', action='store_true', help='Collects specs')

def pytest_collect_file(path, parent):
    if parent.config.option.specs and path.ext == '.py' and path.strpath.find('_spec.py') != -1:
        return SpecFile(path, parent)

class SpecFile(pytest.File):
    def collect(self):
        collector = Runner()

        module = imp.load_source(os.path.basename(self.fspath.purebasename), self.fspath.strpath)
        for _, context in inspect.getmembers(module, inspect.isclass):
            if issubclass(context, Context):
                for ctx, example, parent in collector.examples(context):
                    yield SpecItem(example.__name__, self, ctx, example)

class SpecItem(pytest.Item):

    def __init__(self, name, parent, ctx, example):
        super(SpecItem, self).__init__(name, parent)
        self.ctx = ctx
        self.example = example

    def runtest(self):
        self.ctx.run(self.example)

    def reportinfo(self):
        describe = self.ctx.__class__.__name__
        it = self.example.__name__
        describe_and_it = "%s => %s" % (describe, it)
        return self.fspath, 0, describe_and_it