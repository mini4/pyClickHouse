class ExprMixin:
    '''
    The mixin class for coding SQL operation of expressions and columns.
    '''
    def __add__(self, other):
        return Expr(self, other, op='+')

    def __sub__(self, other):
        return Expr(self, other, op='-')

    def __mul__(self, other):
        return Expr(self, other, op='*')

    def __truediv__(self, other):
        return Expr(self, other, op='/')

    def __lt__(self, other):
        return Expr(self, other, op='<')

    def __le__(self, other):
        return Expr(self, other, op='<=')

    def __gt__(self, other):
        return Expr(self, other, op='>')

    def __ge__(self, other):
        return Expr(self, other, op='>=')

    def __eq__(self, other):
        return Expr(self, other, op='=')


class Expr(ExprMixin):
    '''
    The class for coding SQL operation.
    '''
    def __init__(self, a, b, op):
        self.a = a
        self.b = b
        self.op = op
