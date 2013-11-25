import inspect

__version__ = '0.1.4'

class EmptyContext(object):
    _let = {}
    _before_hooks = []
    _after_hooks = []

class Runner(object):

    def __init__(self):
        self.collected = []

    def run(self, context):
        for ctx, example, parent in self.examples(context):
            ctx.run(example)

    def examples(self, context):
        self.collected = []
        self.collect_from_context(context)

        return self.collected

    def collect_from_context(self, context, parent_context=EmptyContext):
        examples, let, hooks, sub_contexts = {}, {}, {}, {}
        for name, the_type in context.__dict__.items():
            if name.find('it_') == 0:
                examples[name] = the_type

            if name.find('let_') == 0:
                let[name[4:]] = the_type

            if name == 'before':
                hooks.setdefault('before', []).append(the_type)

            if name == 'after':
                hooks.setdefault('after', []).append(the_type)

            if inspect.isclass(the_type):
                sub_contexts[name] = the_type

        for name, example in examples.items():
            ctx = context(parent_context, let, hooks)
            self.collected.append((ctx, example, parent_context))

        for name, sub_context in sub_contexts.items():
            new_parent_context = context(parent_context, let, hooks)
            self.collect_from_context(sub_context, new_parent_context)

class Context(object):

    def __init__(self, parent_context=EmptyContext, let={}, hooks={}):
        self.parent = parent_context

        self._let = dict(self.parent._let.items() + let.items())
        self._before_hooks = self.parent._before_hooks + hooks.setdefault('before', [])
        self._after_hooks = self.parent._after_hooks + hooks.setdefault('after', [])

    def __getattr__(self, attr):
        if attr in self._let:
            return self._attr(attr)

        if self.parent:
            return getattr(self.parent, attr)

        raise AttributeError("Attribute %s not found" % attr)

    def _attr(self, attr):
        value = self._let[attr](self)
        setattr(self, attr, value)

        return getattr(self, attr)

    def run(self, example_method):
        for before in self._before_hooks:
            before(self)
        example_method(self)
        for after in reversed(self._after_hooks):
            after(self)

def run_all(contexts):
    runner = Runner()
    for ctx in contexts:
        runner.run(ctx)