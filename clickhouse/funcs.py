from .expr import ExprMixin


class _FType(type):
    def __getattr__(cls, name):
        return cls(name)


class F(ExprMixin, metaclass=_FType):
    def __init__(self, name, *args):
        self.name = name
        self.args = args  # tuple of tuples

    def __call__(self, *args):
        return F(self.name, *self.args, args)
