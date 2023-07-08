from clickhouse.expr import Expr


def test_expr():
    one = Expr(1, 2, '+')
    two = Expr(3, 4, '+')
    assert (one + two).op == '+'
    assert (one - two).op == '-'
    assert (one * two).op == '*'
    assert (one / two).op == '/'
    assert (one < two).op == '<'
    assert (one <= two).op == '<='
    assert (one > two).op == '>'
    assert (one >= two).op == '>='
    assert (one == two).op == '='
